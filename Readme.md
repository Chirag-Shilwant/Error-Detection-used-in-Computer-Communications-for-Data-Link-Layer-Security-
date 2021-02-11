## SNS ASSIGNMENT-2:
One way communication channel in which one or more threads can send message to a server. The message is encrypted using a specific encoding scheme and the CRC is calculated . The CRC is again calculated at the server side too, to check the authencity of the message.

The folder contains 2 files:
1. **client.py** 
2. **server.py** 

Multiple-clients can send message to the Server. The message will be sent to the server with encryption and the server will display the message.

## To run the server file:
- **python3 server.py**

## To run the client file:
- **python3 client.py**

##### Modules to be installed before running above files:
- pip3 install crccheck - For computing the crc on input message

### Assumptions:
- Input Message should not contain spaces at the end.

