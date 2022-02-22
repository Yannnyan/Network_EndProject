import tkinter as tk
from functools import partial
from CLIENT import Client

window = tk.Tk()
window.geometry("700x500")

client_name: str = None
client: Client.Client_ = None
global isOnline
isOnline = False


# This function is used when pressing the button a popup appears to receive user information about the name of the
# client
def startClient():
    getName()
    client = Client.Client_()


def pressEnter(win, name):
    global client_name
    win.destroy()
    client_name = name.get()
    print(client_name)

def getName():
    top = tk.Toplevel(window)
    top.geometry("100x50")
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
    func = partial(pressEnter, top, name)
    but = tk.Button(top, text="OK", command=func)
    but.pack(side=tk.TOP)
    top.mainloop()


def connectClient():
    global client, client_name, isOnline
    if client_name is None:
        print("Client name not entered. Please enter the client's name to connect and try again.")
        getName()
    else:
        # client.connect(client_name)
        isOnline = True


def disconnectClient():
    global isOnline
    if isOnline is True:
        client.disconnect()
        isOnline = not isOnline


def showChat():
    top = tk.Toplevel()
    top.lift()
    top.attributes("-topmost", True)
    top.geometry("600x400")
    scrollbar = tk.Scrollbar(top)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)


def chatClient():
    global isOnline
    if isOnline is not False:
        showChat()
    else:
        print("Client is disconnected. Please connect client first.")


button_startClient = tk.Button(window, text="Start Client", command=startClient)
button_startClient.grid(row=0, column=0, padx=10)
button_connect = tk.Button(window, text="Connect", command=connectClient)
button_connect.grid(row=0, column=1, padx=10)
button_disconnect = tk.Button(window, text="Disconnect", command=disconnectClient)
button_disconnect.grid(row=0, column=2, padx=10)
button_chat = tk.Button(window, text="Chat", command=chatClient)
button_chat.grid(row=0, column=3, padx=10)
window.mainloop()
