#!/usr/local/bin/python3.5

import socket
import threading





hostname = input(str("Enter the name of host: "))
#port = 8080

def connect(hostname):
    global s
    s=socket.socket()
    port = 8080
    s.connect((hostname,port))
    print("You are now connected to host ",hostname)


def send(msg):
     n = 0
     while n!=1:
         message = msg
         message = message.encode()
         s.send(message)
         #print("Message sent")


def receieve():
        m = 0
        while m!=1:
            imessage = s.recv(1024)
            imessage = imessage.decode()
            print(hostname," : ",imessage)
            print("\n")
            
x = threading.Thread(target = send)
y = threading.Thread(target = receieve)

x.start()
y.start()



