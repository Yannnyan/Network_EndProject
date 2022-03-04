# Network_EndProject
This is our final project in networking course.

# Preview
In this project we built a client server model to represent a chat, in which users can communicate and send files.
The main purpose of this project is to more experienced with using tcp sockets, and building reliable data transfer protocols with congestion control to send files with.


# Our Idea
our idea is to implement RDT that supports the ARQ protocol [Selective repeat](https://en.wikipedia.org/wiki/Selective_Repeat_ARQ). </br>

# How we've done it
## Class Fields
The RDTServer.RDT class consists of few fields. Such as:
| Description\Field | Sequence number | running | window size | timeout | Timer| receivingThread | sendingThread | packets | sendAgain |
|-|-|-|-|-|-|-|-|-|-|
| ~ | The current message's sequence number | bool- Is the server running or not | The maximum amount of new packets that could be sent at specific time | The amount of time a thread waits before resending a packet| Thread that resends the packets again | Thread that listens to the client's messages | Thread that sends new messages to the client based on the window size | Dict stores last packets sent | Minimum heap that stores tuple of time to be sent and sequence number, sorted by time to be sent |
----------------------------------------------------
## Packet Contruction
- Each time the server wants to send a message it constructs a packet consists of few fields that help the client digest the data inside the packet.
- The server fills the sequence field inside the packet with its current sequence number.
- Each packet is filled with 1024 bytes exactly. This is done to prevent the data from being merged into another received packet at the client side, and vice versa.
- To transfer data we used a field called Data to store a buffer sized at most 1024 bytes but could be lower depends on the size of the fields.
- In order to identify the purpose of the packet we used a field named Type, which could consist of the following values: new- new packet, stop- stop sending, req- request ack.
- The most important is the checksum field to address the white elephant in the room, which is data curroption. We've used 16 bits checksum which has 99.98% chance to detect errors.

Every message should look something like this: 
![image](https://user-images.githubusercontent.com/82415308/156677825-793ce11e-ec5a-475c-9f8a-9aa27cf7d490.png)

## Threads

## ARQ System

## Congestion control protocol

![image](https://user-images.githubusercontent.com/82415308/156571449-d71d3f5f-9992-4ae4-b043-ca1b609f1180.png)

The congestion control supports the algorithm which is similar to the Reno tcp protocol. </br>

In the following picture, we can see the change in window size as packets are received over time. Whenever a packet is lost the window size cuts by half.
![image](https://user-images.githubusercontent.com/82415308/156570470-f63fc904-0865-4eed-a4ef-83b7cb81c530.png)


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





