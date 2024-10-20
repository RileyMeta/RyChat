import socket
import datetime
import threading

is_running = True

HOST, PORT = '127.0.0.1', 55550
FORMAT = 'utf-8'

clients = []
nicknames = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Server is listening on {HOST}:{PORT}")

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    index = clients.index(client)
    nickname = nicknames[index]
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    while is_running:
        try:
            # Broadcsting Messages
            message = client.recv(1024)
            format_message = f"[{timestamp}] {nickname}: {message.decode()}".encode(FORMAT)
            print(format_message.decode(FORMAT))
            broadcast(format_message)
        except:
            clients.remove(client)
            client.close()
            broadcast(f"{nickname} has left the chat.".encode(FORMAT))
            nicknames.remove(nickname)
            break

def receive():
    while is_running:
        # Accept new Connections
        client, address = server.accept()

        # Request and store Nicknames
        client.send('NICK'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        nicknames.append(nickname)
        clients.append(client)

        # Print connection to console
        print(f"{nickname} joined from {str(address)}")
        
        broadcast(f"{nickname} has joined the chat!".encode(FORMAT))
        client.send(f"Successfully connected to the server!".encode(FORMAT))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()
