# Network_EndProject
# Preview
In this project we built a client server model to represent a chat, in which users can communicate and send files.
The main purpose of this project is to experience and build reliable data transfer protocols with congestion control to send files with.


# Our Idea
Our idea is to create a multi threaded SERVER implementation for this project. Each client receives a thread that listens to the connection that runs on the server side. When a client wants to download a file it creates a new-ported udp socket and the server creates one too, then they verify the ports with a tcp message. To secure no port duplicates we dedicated 15 unique ports for the client, and 15 unique ports for the server (in practice the server needs more but we don't intend to make more than 7 clients). To manage the ports we creates a file that contains open ports and a port manager wich acts as a garbage collector for ports. The server manages all the information about the clients and listens to new connections and to already existing ones. How we intend to transfer packets with the udp protocol in a reliable and fast way? we've implemented RDT that supports Automatic Repeat Requests system [Selective repeat](https://en.wikipedia.org/wiki/Selective_Repeat_ARQ) but we added a little extension to it, we used dynamic window size.  For more detail, we've implemented The algorithms : slow start, congestion avoidance, FAST recovery. </br> 
</br>

-------

## links to server and client </br>
[SERVER](https://github.com/Yannnyan/Network_EndProject/blob/main/SERVER/Server.py) </br>
[CLIENT](https://github.com/Yannnyan/Network_EndProject/blob/main/CLIENT/Client.py) </br>
[GUI](https://github.com/Yannnyan/Network_EndProject/blob/main/CLIENT/ClientGUI.py)

--------

## How to run
1. download the directory to your pc.
2. open terminal, and path to the SERVER directory.
3. type python3 Server.py
4. open another terminal window, and path to the CLIENT directory.
5. type python3 ClientGUI.py
- its important to run the app from inside of the directoriess specified above.

# How we've done it
## UML
This uml represents how our system works most basically. </br>
![image](https://user-images.githubusercontent.com/82415308/156893960-b5e37ccc-b556-42dd-bbfb-92ce2dd5e8de.png)


## Download file from Server
- The Client opens a udp socket and our RDT implemented class, and listens to it. 
- Then it sends a TCP message to the server asking to download a specific file.
-  The server responds with one of two ways depends whether the client already asked to download a file or not. It opens a udp socket and saves it or resets parameters. 
-  The server then sends a SYN with the name of the file to the client's listening socket.
-  The client sends back SYN-ACK with the number of bytes already ACKNOWLEGED.
-  The server then redirects the file pointer to the current byte and starts sending the file again.
## ARQ System
- The Server sends a packet formatted as specified above.
- The client responds with ACK with the packet is received successfully. Or with NACK if the packet is corrupted. If it failed to read the packet it does nothing and wait for the server to resend the packet.
## Reliablility
- The serverRDT class represents the handler for the udp reliable data transfer. It sends and receives all the messages associated with udp.
- The serverRDT contains data structures to track the acknowledged packets. A dict of sequence number followed by a packet - tracks the unacknowledged packets. A minimum heap sorted by the time to send the packet, with value of sequence number of the unacknowledged packed.
- A thread is running in the background and checking if data needs to be retransmitted by checking the length of the dict, if data needs to be retransmitted it goes to the heap and peeks and sends the minimum while the time to send the packets has passed, then increases the key of the resent packet by a set timeout seconds. </br> In the following picture we can see how the selective repeat algorithm operates upon lost packets and how it provides reliabillity. We can see similarities between this algorithm and between our algorithm, when we fix a cwnd size untill all packages are received. This way we can ensure all packages are received, since we keep resending lost packages untill we receive ack about them from the client.
![image](https://user-images.githubusercontent.com/82415308/156571449-d71d3f5f-9992-4ae4-b043-ca1b609f1180.png)
## Congestion control
CC UML </br>
![image](https://user-images.githubusercontent.com/82415308/156896281-c4cc9986-df73-4b42-a74f-88e40f084a3f.png)

- The serverRDT class contains an object of Congestion Control class, which handles the congestion window size by receiving ACKS or LOST messages.
- our congestion control algorithm does not change the packet size at all.
- slow start algorithm - start with cwnd of size 2, meaning that we can send only 2 packets. If the number of consecutive sequence ACKS is greater or equal to the cwnd size, then multiply the cwnd by 2.
- ResetCWND - if we encounter a LOST at any point we will decrease the cwnd size times 1/2 and set the current thresh to be cwnd times 1/2. Once we encountered a loss we will not return to slow start algorithm.
- Congestion avoidance - 
The congestion control supports an algorithm which is similar to the Reno tcp protocol. </br>
In the following picture, we can see the change in window size as packets are received over time. Whenever a packet is lost the window size cuts by half, and the thresh is set to half the window size too. In our implementation we see similarity in these two properties. Additionaly to congestion avoidance and fast recovery, we also implemented slow start algorithm, that initializes the thresh faster than the congestion avoidance algorithm to check where is the limit for maximum packet sending speed.
![image](https://user-images.githubusercontent.com/82415308/156570470-f63fc904-0865-4eed-a4ef-83b7cb81c530.png)
## Data Integrity
- To provide some security for the packets, we've created a regular 16 bit checksum algorithm. </br>
The Algorithm process: 
- The buffer is converted to bits by concatinating 8 bit ascii values of the characters and padding with zeros.
- The Sender side takes the buffer and divides it into groups of 16 bits
- Then it adds all of them together, and adds back the carry if there is one.
- Then send the 16 bit number as checksum.
- The receiver side takes the buffer and does the same process that specified above, and then adds the checksum that the sender sent.
- if the result contains a zero then there was data corruption.
- ** Note that this algorithm only provides some protection while some errors can go undetected **
## Packet Construction
- Each time the server wants to send a message it constructs a packet consists of few fields that help the client digest the data inside the packet.
- The server fills the sequence field inside the packet with its current sequence number.
- Each packet is filled with 1024 bytes exactly. This is done to prevent the data from being merged into another received packet at the client side, and vice versa.
- To transfer data we used a field called Data to store a buffer sized at most 1024 bytes but could be lower depends on the size of the fields.
- In order to identify the purpose of the packet we used a field named Type, which could consist of the following values: new- new packet, stop- stop sending, req- request ack.
- The most important is the checksum field to address the white elephant in the room, which is data curroption. We've used 16 bits checksum.

Every message should look something like this: 
![image](https://user-images.githubusercontent.com/82415308/156677825-793ce11e-ec5a-475c-9f8a-9aa27cf7d490.png)
## Class Fields
The RDTServer.RDT class consists of few fields. Such as:
| Description\Field | Sequence number | running | window size | timeout | Timer| receivingThread | sendingThread | packets | sendAgain |
|-|-|-|-|-|-|-|-|-|-|
| ~ | The current message's sequence number | bool- Is the server running or not | The maximum amount of new packets that could be sent at specific time | The amount of time a thread waits before resending a packet| Thread that resends the packets again | Thread that listens to the client's messages | Thread that sends new messages to the client based on the window size | Dict stores last packets sent | Minimum heap that stores tuple of time to be sent and sequence number, sorted by time to be sent |
----------------------------------------------------
## CLIENT SERVER TCP communication and packets
- The Client connects to the server, the server saves it's connection inside a dictionary by the client's address.
- The Client sends requests in form of tcp packets, where the data contains a command and value, which then the server can analize and respond accordingly.
- The general data format of a packet is {"command" : "value"}, we use json library to analize the messages.
- When a client wants to disconnect from the service, it sends a disconnect message {"dc", ""} , then the server removes him from all the data structures he is stored. and closes the socket.
### Threads
- The threads are part of the client server communication. 
- The client opens a listening thread that receives messages from the server and update the gui accordingly.
- The Server on the other hand has a thread for each client, that listens to the client's messages on it's connection socket. And another thread to accept new connections from the clients.
## GUI
![image](https://user-images.githubusercontent.com/82415308/156894099-8f4c6a1c-60fb-466a-a5cc-e0a9f90abbb0.png)
![image](https://user-images.githubusercontent.com/82415308/156894210-b5843895-ecb3-47e1-b545-e95f18b0d6ef.png)
![image](https://user-images.githubusercontent.com/82415308/156894259-40b75670-4bbc-486e-b2e3-baa80b21cfbd.png)
![image](https://user-images.githubusercontent.com/82415308/156894286-c38569b5-3e0b-4c06-bca4-f566c555cacd.png)
![image](https://user-images.githubusercontent.com/82415308/156894315-c2f85d83-fc46-4ec9-836f-76ebac44e4cd.png)
![image](https://user-images.githubusercontent.com/82415308/156894393-05ee23c3-eb01-4e6c-9634-41cac3b07299.png)


