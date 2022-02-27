import json
import threading
from threading import Timer
import tkinter as tk
from tkinter import ttk
from functools import partial
from CLIENT import Client

window = tk.Tk()
window.title("Main Menu")
window.geometry("800x500")

serveraddress: str = None
client_name: str = None
client: Client.Client_ = None
onlineClients = None
isOnline = False

listeningThread = None
timer = None

updateLogText = "Update Log"


# This function is used when pressing the button a popup appears to receive user information about the name of the
# client

def listenClient():
    while isOnline:
        message = client.listenClient()
        getMessageFromClient(message)


# starts the thread to listen the listen to messages the client is receiving
def startClient():
    global client_name, serveraddress, client
    if isOnline is True:
        print("Client is already connected. You cannot start another client.")
        return
    getName()
    if client_name is not None and serveraddress is not None:
        client = Client.Client_(serveraddress, client_name)


def checkValidAddress(address: str) -> bool:
    div: list = address.split('.')
    if len(div) != 4:
        return False
    else:
        for dim in div:
            try:
                val = int(dim)
                if val > 255 or val < 0:
                    return False
            except ValueError:
                return False
        return True


def clientGetUsers():
    client.get_users()


def pressOK(win, name, addressVar):
    global client_name, serveraddress
    address: str = addressVar.get()
    if address == "localhost":
        serveraddress = "127.0.0.1"
        client_name = name.get()
        print(client_name)
        win.quit()
    elif checkValidAddress(address) is True:
        serveraddress = address
        client_name = name.get()
        print(client_name)
        win.quit()
    else:
        print("Address is not valid. Try again.")


def getName():
    top = tk.Toplevel(window)
    top.title("Info")
    top.geometry("250x250")
    top.lift()
    top.attributes("-topmost", True)
    win_x = window.winfo_x() + 300
    win_y = window.winfo_y() + 100
    top.geometry(f'+{win_x}+{win_y}')

    label = tk.Label(top, width=15, text="Enter client's name")
    label.pack(side=tk.TOP)

    name = tk.StringVar()
    nameEntered = tk.Entry(top, width=15, textvariable=name)
    nameEntered.pack(side=tk.TOP)

    label1 = tk.Label(top, width=15, text=" Enter Server's address")
    label1.pack(side=tk.TOP)

    address = tk.StringVar()
    addressEntered = tk.Entry(top, width=15, textvariable=address)
    addressEntered.pack(side=tk.TOP)

    func = partial(pressOK, top, name, address)
    but = tk.Button(top, text="OK", command=func)
    but.pack(side=tk.TOP)
    top.mainloop()
    top.destroy()


def connectClient():
    global client, client_name, serveraddress, isOnline
    if isOnline is True:
        return
    if client_name is None or serveraddress is None:
        print("Client name or server address not entered. Please enter the details to connect and try again.")
        getName()
    else:
        if isOnline is False:
            client.connect()
            isOnline = True
            listeningThread = threading.Thread(target=listenClient)
            listeningThread.start()



def disconnectClient():
    global isOnline, listeningThread
    if isOnline is True:
        isOnline = not isOnline
        client.disconnect()
        # listeningThread


def _from_rgb(rgb):
    r, g, b = rgb
    return f'#{r:02x}{g:02x}{b:02x}'


# func that creates a chat pop up to show the messages of the clients
def showChat():
    chat = tk.Toplevel()
    chat.title("Chat")
    chat.lift()
    chat.attributes("-topmost", True)
    chat.geometry("600x400")

    top = tk.Frame(chat)
    top.pack(side=tk.TOP)
    bottom = tk.Frame(chat)
    bottom.pack(side=tk.BOTTOM)

    scrollbary = tk.Scrollbar(chat)
    scrollbary.pack(in_=top, side=tk.RIGHT, fill=tk.Y)
    scrollbarx = tk.Scrollbar(chat, orient=tk.HORIZONTAL)
    scrollbarx.pack(in_=top, side=tk.BOTTOM, fill=tk.X)

    chatText = tk.Text(chat, width=70, height=20, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    chatText.configure(bg=_from_rgb((76, 230, 52)))
    chatText.pack(in_=top, side=tk.LEFT)
    scrollbary.config(command=chatText.yview)
    scrollbarx.config(command=chatText.xview)

    textBox = tk.Entry(chat, text="")
    textBox.pack(in_=bottom, side=tk.RIGHT)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TCombobox", fieldbackground="orange", background="white")
    comboBox = ttk.Combobox(chat, width=20)
    comboBox.pack(in_=bottom, side=tk.LEFT)

    comboBox['values'] = onlineClients
    comboBox.set("See online")
    comboBox['state'] = 'readonly'

    chat.mainloop()


def chatClient():
    global isOnline
    if isOnline is not False:
        showChat()
    else:
        print("Client is disconnected. Please connect client first.")


def showOnlineList():
    toplist = tk.Tk()
    toplist.geometry("400x400")
    toplist.lift()
    toplist.attributes("-topmost", True)
    listOnline = tk.Listbox(toplist, width=50)
    listOnline.pack(side=tk.TOP, pady=10)
    for i in range(len(onlineClients)):
        listOnline.insert(i, onlineClients[i])
    toplist.mainloop()


# Client sends a message to the gui with the command and the description to be executed and the gui reacts to display
# that.
def getMessageFromClient(message: str):
    print("[CLIENT] got message from server. " + message)
    # '{"command" : "description"}'
    d: dict = json.loads(message)
    ex = list(d.keys())[0]
    val = list(d.values())[0]
    print(d)
    print(ex)
    print(val)
    if ex == 'whoOnline':
        global onlineClients
        onlineClients = val
        mes = ''
        for i in range(len(val)):
            mes += val[i]
            if i != len(val) - 1:
                mes += ', '
        showOnlineList()
        updateLog("Users Online:", mes)

    if ex == 'connect':
        updateLog("User Connected", val + " has connected to the server.")
    if ex == "dc":
        updateLog("User Disconnected", client_name + " has disconnected from the server.")
    if ex == "msg":
        updateLog("User message", client_name + " has sent message to " + val)
    if ex == "msgall":
        updateLog("User message all", client_name + " has sent message to everyone online.")
    if ex == "files":
        updateLog("Files available", ', '.join(val))


# updates the label that shows all the recent changes
def updateLog(title: str, message: str):
    global updateLogText
    updateLogText += "\n" + "------- " + title + " -------" + "\n" + message


def updateComponents():
    global window, isOnline
    # print("second has passed")
    label_recentChanges.configure(text=updateLogText)
    # if isOnline is True:
    window.after(1000, updateComponents)


# function that closes all threads when exiting the client gui
def close_window():
    global window, timer, listeningThread, isOnline, client
    isOnline = False
    if client is None:
        window.destroy()
        return
    client.disconnect()
    window.destroy()


# buttons
button_startClient = tk.Button(window, text="Start Client", command=startClient)
button_startClient.grid(row=0, column=0, padx=10)
button_connect = tk.Button(window, text="Connect", command=connectClient)
button_connect.grid(row=0, column=1, padx=10)
button_disconnect = tk.Button(window, text="Disconnect", command=disconnectClient)
button_disconnect.grid(row=0, column=2, padx=10)
button_showOnline = tk.Button(window, text="Show Online", command=clientGetUsers)
button_showOnline.grid(row=0, column=3, padx=10)
button_showFiles = tk.Button(window, text="Show files")
button_showFiles.grid(row=0, column=4, padx=10)
button_chat = tk.Button(window, text="Chat", command=chatClient)
button_chat.grid(row=0, column=5, padx=10)
# labels
label_recentChanges = tk.Label(window, width=30, height=20, anchor=tk.N, text="Update log")
label_recentChanges.config(bg="gray")
label_recentChanges.grid(row=1, column=0, padx=10, pady=5)
# timers, operations on window
window.after(1000, updateComponents)
window.wm_protocol("WM_DELETE_WINDOW", close_window)

window.mainloop()
