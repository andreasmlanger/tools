"""
This script demonstrates a basic server-client interaction using the socket module.
It sets up a server that listens for incoming connections and spawns a new thread to handle each client.
The server receives messages from clients, prints them, and responds with a confirmation message.
Start 'socket_server.py' in PyCharm, then open Anaconda prompt and start client with 'python socket_client.py'.
"""

import socket
import threading

HEADER = 16
PORT = 5050
COMPUTER_NAME = socket.gethostname()
SERVER = socket.gethostbyname(COMPUTER_NAME)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')
    while True:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
        except (ConnectionResetError, OSError):
            print('[DISCONNECTED]')
            conn.close()
            break
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            print(f'[{addr}] {msg}')
            conn.send('Message received'.encode(FORMAT))


def start():
    server.listen()
    print(f'[LISTENING] Server is listening on {SERVER} | {COMPUTER_NAME}')
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        print(f'[ACTIVE CONNECTIONS] {threading.active_count()}')
        thread.start()


start()
