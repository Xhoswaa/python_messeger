from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from datetime import datetime

addresses = {}
clients = {}

IP = '127.0.0.1'
PORT = 5555
HEADERLEN = 8
HOST = (IP, PORT)


def write_to_logs(text):
    date = datetime.now().strftime('%d-%m-%Y')
    time = datetime.now().strftime('%H:%M:%S')
    with open(f'logs/{date}.log', 'a') as logs:
        logs.write(f'[{time}] {text}\n')

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

def accept_connections():
    while True:
        client, address = server.accept()
        print(f'{address} successfully connection')
        write_to_logs(f'{address[0]}:{address[1]} successfully connected')
        #optimize_send(client, 'enter your username'.encode('utf8'), HEADERLEN)
        addresses[client] = address
        Thread(target=handle_client, args=(client,)).start()

def handle_client(client):
    try:
        name = optimize_recv(client, HEADERLEN).decode('utf8')
        optimize_send(client, f'welcome, {name}!'.encode('utf8'), HEADERLEN)
        msg = f'{name} join the correspondence'.encode('utf8')
        broadcast(msg)
        write_to_logs(f'{addresses[client][0]}:{addresses[client][1]} set name to "{name}"')
        clients[client] = name

        while True:
            try:
                msg = optimize_recv(client, HEADERLEN)
                prefix = name+': '
                broadcast(msg, prefix)
                write_to_logs(f'{addresses[client][0]}:{addresses[client][1]} "{name}" send "{msg.decode('utf8')}"')
            except:
                client.close()
                del clients[client]
                broadcast(f'{name} left the correspondence'.encode('utf8'))
                print(f'{addresses[client]} has disconnected')
                write_to_logs(f'{addresses[client][0]}:{addresses[client][1]} has disconnected')
                break
    except:
        client.close()
        print(f'{addresses[client]} has disconnected')
        write_to_logs(f'{addresses[client][0]}:{addresses[client][1]} has disconnected')
        del addresses[client]

def broadcast(msg, prefix=''):
    for sock in clients:
        optimize_send(sock, prefix.encode('utf8') + msg, HEADERLEN)


server = socket(AF_INET, SOCK_STREAM)
server.bind(HOST)
write_to_logs(f'server is running on {IP}:{PORT}')

server.listen(5)
print('listen for connections...')
accept_thread = Thread(target=accept_connections)
accept_thread.start()
accept_thread.join()