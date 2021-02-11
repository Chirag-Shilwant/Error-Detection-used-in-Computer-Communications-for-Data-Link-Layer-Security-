import sys
import socket
import numpy as np
from crccheck.crc import Crc32, CrcXmodem
import pickle

PORT = 1234
IP = "127.0.0.1"

A = np.array([ [-3, -3, -4],
    [0, 1, 1],
    [4, 3, 4]
])

def notMultiple(inputMessage):
    if len(inputMessage) % 3 != 0:
        return 1
    return 0


def encodeKar(inputMessage,A):
    list1 = list()
    data1 = list()
    
    while notMultiple(inputMessage): 
        inputMessage += " "
    
    list1=[(ord(ch)-65+1) for ch in inputMessage]
    
    list1[:] = [x if x != -32 else 27 for x in list1]

    arr2 = np.reshape(np.array(list1), (3, len(list1)//3), 'F')
    
    print(arr2)

    return np.dot(A,arr2) 

s = socket.socket()
s.connect((IP, PORT))

while(True):
    inputMessage = str(input())
    encryptedmessage = encodeKar(inputMessage,A)

    inputMessage = ''.join(format(i, 'b') for i in bytearray(inputMessage, encoding ='utf-8')) 
    
 
    crcgenerated = Crc32.calc(bytearray(inputMessage,encoding = 'utf-8'))
    
    crcgenerated = str(crcgenerated).encode('utf-8')
    
    print("Connection established with server")
    s.send(pickle.dumps(encryptedmessage))
    print(s.recv(1023).decode())
    s.send(crcgenerated)
    print(s.recv(1023).decode())
    print("\n\n")
s.close()