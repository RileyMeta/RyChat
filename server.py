import socket
import datetime
import threading

is_running = True

HOST, PORT = '127.0.0.1', 55555
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

def shutdown(client):
    index = clients.index(client)
    clients.remove(client)
    client.close()
    nickname = nicknames[index]
    nicknames.remove(nickname)

def get_timestamp():
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    return timestamp

def handle(client):
    index = clients.index(client)
    nickname = nicknames[index]

    while is_running:
        try:
            # Broadcsting Messages
            message = client.recv(1024)
            if message.decode(FORMAT) == '/quit':
                shutdown(client)
            format_message = f"[{get_timestamp()}] {nickname}: {message.decode()}".encode(FORMAT)
            print(format_message.decode(FORMAT))
            broadcast(format_message)
        except:
            shutdown(client)
            break

def receive():
    while is_running:
        # Accept new Connections
        client, address = server.accept()

        # Request and store Nicknames
        client.send('<NICK>'.encode(FORMAT))
        nickname = client.recv(1024).decode(FORMAT)
        nicknames.append(nickname)
        clients.append(client)

        # Print connection to console
        print(f"{nickname} joined from {str(address[0])}:{str(address[1])}")
        
        broadcast(f"{nickname} has joined the chat!".encode(FORMAT))
        client.send(f"Successfully connected to the server!".encode(FORMAT))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()
