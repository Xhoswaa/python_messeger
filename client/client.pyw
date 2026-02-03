from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import *
from tkinter import ttk

connect = {}
with open('connect.txt', 'r', encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if line and '=' in line:
            key, value = line.split('=', 1)
            connect[key.strip()] = value.strip()

def optimize_recv(client, headerlen):
    data_header = client.recv(headerlen)
    data_len = int(data_header.strip())
    data = client.recv(data_len)
    return data

def optimize_send(client, data, headerlen):
    data_header = f'{len(data):<{headerlen}}'
    data = data.decode('utf8')
    data = data_header + data
    client.send(data.encode('utf8'))

def msg_receive():
    while True:
        msg = optimize_recv(client, HEADERLEN).decode('utf8')
        msg_list.insert(END, msg)
        msg_list.yview_moveto(1.0)

def msg_send(event=None):
    msg = my_msg.get()
    if msg:
        my_msg.set('')
        optimize_send(client, msg.encode('utf8'), HEADERLEN)

def on_closing():
    client.close()
    root.destroy()

#tkinter
root = Tk()
root.geometry('400x300')
root.title('messenger')

messages_frame = ttk.Frame(root)
messages_frame.place(relx=0, rely=0, relwidth=1, relheight=0.965)

my_msg = StringVar()
my_msg.set('')

scrollbar = ttk.Scrollbar()
scrollbar.place(relx=1, rely=0, relheight=0.87, anchor='ne')

msg_list = Listbox(messages_frame, yscrollcommand=scrollbar.set)
msg_list.place(relx=0, rely=0, relwidth=1, relheight=0.9)

entry_field = ttk.Entry(root, textvariable=my_msg)
entry_field.bind('<Return>', msg_send)
entry_field.place(relx=0, rely=0.87, relwidth=0.91, relheight=0.13)
send_button = ttk.Button(root, text='>', command=msg_send)
send_button.place(relx=0.9, rely=0.87, relwidth=0.1, relheight=0.13)

root.protocol('WM_DELETE_WINDOW', on_closing)


#socket
IP = connect['ip']
PORT = int(connect['port'])
HEADERLEN = 8
HOST = (IP, PORT)

client = socket(AF_INET, SOCK_STREAM)
client.connect(HOST)

optimize_send(client, connect['username'].encode('utf8'), HEADERLEN)

#bebebebububu
receive_thread = Thread(target=msg_receive)
receive_thread.start()
send_thread = Thread(target=msg_send)
send_thread.start()
root.mainloop()