#!/usr/bin/python3.5
import tkinter
import threading
import socket
    
root = tkinter.Tk()
root.maxsize(700,700)
root.title("Messenger-Client")

label_1 = tkinter.Label(root,text="Enter Host name: ")
host=tkinter.StringVar()
send_msg=tkinter.StringVar()
s=socket.socket()

    
e = tkinter.Entry(root,textvariable=host)
#chatFrame = tkinter.Frame(root)

def getHostname():
    global send_box
    global w
    host = e.get()
    connect(host)
    label_2 = tkinter.Label(root,text="You are conncted to "+host)
    label_2.pack()
    #chatFrame.grid(rowspan=10,columnspan=10)
    w = tkinter.Text(root)
    w.pack()
    bottomframe = tkinter.Frame(root,width=300,height=50)
    bottomframe.pack()
    send_box = tkinter.Entry(bottomframe,textvariable=send_msg)
    #send_msg = send_box.get()
    send_box.pack()
    send_btn = tkinter.Button(bottomframe,text='Send',command = send_func)
    send_btn.pack()
    print("Reached here")
    x = threading.Thread(target = send_func)
    y = threading.Thread(target = receieve)
    x.start()
    y.start()
    
def send_func():
    send_msg = send_box.get()
    send_msg_new = str(send_msg)
    send(send_msg_new)
    w.insert(0.0,'You : %s \n' % send_msg_new )
    send_box.delete(0,tkinter.END)
     

def receieve():
	m = 0
	while m != 1:
		imessage = s.recv(1024)
		imessage = imessage.decode()
		print(imessage)
		print("\n")
		w.insert(0.0,'Other : %s \n' % imessage )  

def connect(hostname):
    port = 8080
    s.connect((hostname,port))
    print("You are now connected to host ",hostname)

def send(msg):
    message = msg
    message = message.encode()
    s.send(message)
    #print("msg sent")


    

connect_btn = tkinter.Button(root,text='Connect',command=getHostname)
    
label_1.pack()    
e.pack()
connect_btn.pack()
    
root.mainloop()
