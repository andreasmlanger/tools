import socket


HEADER = 16
PORT = 5050
FORMAT = 'utf-8'
SERVER = '192.168.137.1'
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    try:
        client.send(send_length)
        client.send(message)
        print(client.recv(2048).decode(FORMAT))
    except ConnectionResetError:
        print('[DISCONNECTED]')


while True:
    send(input())
