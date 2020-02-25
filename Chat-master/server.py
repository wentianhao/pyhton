#import tkinter
import socket 
#import time 
#import sys
import threading


s = socket.socket()
host = socket.gethostname()
print("\n")
print("Starting server on : ", host)

port = 8080
s.bind((host,port))

print("Waiting for someone to join...")
print(host)

s.listen(1)
conn,addr=s.accept()
print(addr,"Has connected to server and is now online")

def send():
        n = 0
        while n!=1:
            message = input("Enter : ")
            message = message.encode()
            conn.send(message)
            #print("Message sent")

def receieve():
        m = 0
        while m!=1:
            message = conn.recv(1024)
            message = message.decode()
            print("other : ",message)
            print("\n")
            
x = threading.Thread(target = send)
y = threading.Thread(target = receieve)

x.start()
y.start()
