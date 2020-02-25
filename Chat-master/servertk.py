#!/usr/bin/python3.5
import tkinter
import threading
import socket

root = tkinter.Tk()
root.maxsize(700,700)
root.title("Messenger-Server")

s = socket.socket()
host = socket.gethostname()
port = 8080
s.bind((host,port))

send_msg = tkinter.StringVar()

def start_server():
	label1=tkinter.Label(root,text="Starting server on : %s"%host)
	label1.pack()
	label2=tkinter.Label(root,text="Waiting for someine to join...")
	label2.pack()
	label3=tkinter.Label(root,text="Click accept and then enter hostname on client device")
	label3.pack()
	accept_btn = tkinter.Button(root,text='Accept',command=accept)
	accept_btn.pack()
	
def accept():
	global conn
	global w
	global send_box
	s.listen(1)
	conn,addr=s.accept()
	addr_new = str(addr)
	label4=tkinter.Label(root,text="%s has now connected and is now online."%addr_new)
	label4.pack()
	w = tkinter.Text(root)
	w.pack()
	bottomframe = tkinter.Frame(root,width=300,height=50)
	bottomframe.pack()
	send_box = tkinter.Entry(bottomframe,textvariable=send_msg)
	send_box.pack()
	send_btn = tkinter.Button(bottomframe,text='Send',command = send_func)
	send_btn.pack()
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
	while m!=1:
		imessage = conn.recv(1024)
		imessage = imessage.decode()
		print(imessage)
		print("\n")
		w.insert(0.0,'Other : %s \n' % imessage )		

def send(msg):
    message = msg
    message = message.encode()
    conn.send(message)

start_btn = tkinter.Button(root,text='Start Server',command=start_server)
start_btn.pack()

root.mainloop()
