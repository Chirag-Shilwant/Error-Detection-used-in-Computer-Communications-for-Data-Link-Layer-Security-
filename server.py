import socket             
import numpy as np
import pickle
from crccheck.crc import Crc32, CrcXmodem
import threading

PORT = 1234

A_Inverse = np.array([[1, 0, 1],
    [4, 4, 3],
    [-4, -3, -3]])

def getOriginaltext(decryptedmessage, A_Inverse):
    matrixDot = np.dot(A_Inverse, decryptedmessage)
    
    matrixDot = matrixDot.transpose()
    
    originalMessage = ""

    for row in matrixDot:
        for c in row:
            if c!=27:
                originalMessage += chr(c+65-1)
            else:
                originalMessage += " "

    return originalMessage.rstrip() 
            
def threaded(c):
    while(True):
        messageMatrix = c.recv(50000)
        c.send("Server recieved your msg".encode('utf-8'))
        if(len(messageMatrix) < 3):
            continue
        
        crcFromClient = c.recv(50000)
        
        crcFromClient = crcFromClient.decode()
        
        messageMatrix = messageMatrix[:messageMatrix[1:].find(b'\x80')]
        messageMatrix += b'.'

        decryptedmessage = pickle.loads(messageMatrix)
        
        originalMessage = getOriginaltext(decryptedmessage, A_Inverse)
        print("Message received from client : ", originalMessage)

        originalMessage = ''.join(format(i, 'b') for i in bytearray(originalMessage, encoding ='utf-8')) 
   
        crcAtServer = Crc32.calc(bytearray(originalMessage,encoding = 'utf-8'))

        if int(crcAtServer) == int(crcFromClient):
            print("Received Message is correct. No error is detected during the communication")
        
        else:
            print("Received Message is incorrect. Error is detected during the communication")
        
        c.send("Transmission over".encode('utf-8'))
        print("\n\n")

s = socket.socket()     
s.bind(('', PORT))        
print ("socket binded to %s" %(PORT))  
s.listen()  
print ("Socket is listening")  
while(True):          
    c, addr = s.accept()
    threading.Thread(target=threaded, args=(c,)).start()
s.close()