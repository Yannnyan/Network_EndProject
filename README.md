# Network_EndProject
# Preview
In this project we built a client server model to represent a chat, in which users can communicate and send files.
The main purpose of this project is to experience and build reliable data transfer protocols with congestion control to send files with.


# Our Idea
our idea is to implement RDT that supports the ARQ system [Selective repeat](https://en.wikipedia.org/wiki/Selective_Repeat_ARQ) but with changing window size that supports the algorithms slow start, congestion avoidance, FAST recovery. </br> 
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
</br> done
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
- The serverRDT class contains an object of Congestion Control class, which handles the congestion window size by receiving ACKS or LOST messages.
- our congestion control algorithm does not change the packet size at all.
- slow start algorithm - start with cwnd of size 2, meaning that we can send only 2 packets. If the number of consecutive sequence ACKS is greater or equal to the cwnd size, then multiply the cwnd by 2.
- ResetCWND - if we encounter a LOST at any point we will decrease the cwnd size times 1/2 and set the current thresh to be cwnd times 1/2. Once we encountered a loss we will not return to slow start algorithm.
- Congestion avoidance - 
The congestion control supports an algorithm which is similar to the Reno tcp protocol. </br>
In the following picture, we can see the change in window size as packets are received over time. Whenever a packet is lost the window size cuts by half, and the thresh is set to half the window size too. In our implementation we see similarity in these two properties. Additionaly to congestion avoidance and fast recovery, we also implemented slow start algorithm, that initializes the thresh faster than the congestion avoidance algorithm to check where is the limit for maximum packet sending speed.
![image](https://user-images.githubusercontent.com/82415308/156570470-f63fc904-0865-4eed-a4ef-83b7cb81c530.png)
## Data Integrity
- To provide some security for the packets, we've created a regular 16 bit checksum algorithm.
The Algorithm process: 
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
## Threads
## CLIENT SERVER TCP communication
## GUI
![image](https://user-images.githubusercontent.com/82415308/156894099-8f4c6a1c-60fb-466a-a5cc-e0a9f90abbb0.png)
![image](https://user-images.githubusercontent.com/82415308/156894210-b5843895-ecb3-47e1-b545-e95f18b0d6ef.png)
![image](https://user-images.githubusercontent.com/82415308/156894259-40b75670-4bbc-486e-b2e3-baa80b21cfbd.png)
![image](https://user-images.githubusercontent.com/82415308/156894286-c38569b5-3e0b-4c06-bca4-f566c555cacd.png)
![image](https://user-images.githubusercontent.com/82415308/156894315-c2f85d83-fc46-4ec9-836f-76ebac44e4cd.png)
![image](https://user-images.githubusercontent.com/82415308/156894393-05ee23c3-eb01-4e6c-9634-41cac3b07299.png)



## Congestion control protocol


# Directories

1. [SERVER](https://github.com/Yannnyan/Network_EndProject/tree/main/SERVER)
2. [CLIENT](https://github.com/Yannnyan/Network_EndProject/tree/main/CLIENT)
3. [FILES](https://github.com/Yannnyan/Network_EndProject/tree/main/FILES)
4. [TESTS](https://github.com/Yannnyan/Network_EndProject/tree/main/TESTS)
5. [Algorithms](https://github.com/Yannnyan/Network_EndProject/tree/main/Algorithms)

# Classes
### SERVER
1. Server - represents the most 

### CLIENT
1. Client - represents the basic client class that communicates with the server.
2. ClientGUI - represent comfortable UI for the user to communicate with the server.
### FILES
> description of the files inside FILES directory
1. txt - text files
2. png - images
3. generateFile.py - Generate files of a certain size. 
4. 
### TESTS
1. Server RDT tests
2. checksum tests
3. congestion control tests

### Algorithms
1. Minheap - basic data structure that enables to decrease key with O log n complexity as opposed to pythons default heap that does not support this operation.
2. checksum - computes the checksum of the buffer given to the checksum and, contains a function that checks whether the checksum received is valid. Allows to verify that the data transfered is valid.
3. 












## Summary of the pdf
> Generally - we need to build a client server communication design in python to send and receive files.
1) gui := bonus.
2) design an implementation for (FAST UDP reliable) + congestion control (RDT).

## Links for devs (Delete Later)
[google docs](https://docs.google.com/document/d/1WFzKAJH9fTqFsBf4oBU_-Y3lwhuzAA75eS2UvtlveAs/edit)

## Project pdf (Delete later)

### Rules
![image](https://user-images.githubusercontent.com/82415308/151711634-42814d03-4c39-45af-bfb1-3b5b05eb9a5f.png)
![image](https://user-images.githubusercontent.com/82415308/151711654-75646717-a2bb-47cd-9aee-c95413ab1669.png)
### The Excersice
![image](https://user-images.githubusercontent.com/82415308/151711581-1cbe4405-df53-4477-8e00-549c81639ac2.png)
![image](https://user-images.githubusercontent.com/82415308/151711700-e9b1023b-ebcf-4b46-86db-22070645c2d5.png)
![image](https://user-images.githubusercontent.com/82415308/151711718-55356b4e-b07a-4c37-a358-9214c5755f60.png)
![image](https://user-images.githubusercontent.com/82415308/151711737-63d01ae3-74ba-4f98-8b28-d8f18572bc69.png)
### Description of the system
![image](https://user-images.githubusercontent.com/82415308/151711758-6232882d-0cce-4ce0-ab12-7185234cffe1.png)
![image](https://user-images.githubusercontent.com/82415308/151711774-212ebe36-bb3a-4133-a9a0-e934a04af2aa.png)
![image](https://user-images.githubusercontent.com/82415308/151711787-553631df-f55a-4aaf-a62d-ba2c9c3dc148.png)
![image](https://user-images.githubusercontent.com/82415308/151711807-4e1c6657-1886-430b-ad23-c314bedb9248.png)
![image](https://user-images.githubusercontent.com/82415308/151711824-dfdc2fce-d753-4160-89f3-19bffe28080a.png)





