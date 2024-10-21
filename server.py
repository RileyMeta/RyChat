import socket
import datetime
import threading

is_running = True
lock = threading.Lock()

HOST, PORT = '127.0.0.1', 55550
FORMAT = 'utf-8'

clients = []
nicknames = []

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()
print(f"Server is listening on {HOST}:{PORT}")

def broadcast(message):
    with lock:  # Ensure no race conditions when sending messages
        for client in clients:
            try:
                client.send(message)
            except Exception as e:
                print(f"Error broadcasting message: {e}")

def shutdown(client):
    with lock:  # Lock while modifying shared resources
        if client in clients:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            client.close()

def get_timestamp():
    return datetime.datetime.now().strftime('%H:%M:%S')

def handle(client):
    with lock:
        index = clients.index(client)
        nickname = nicknames[index]

    while is_running:
        try:
            message = client.recv(1024)
            if message.decode(FORMAT) == '/quit':  # Correct byte-to-string comparison
                shutdown_message = f"[{get_timestamp()}] {nickname} has left the chat.".encode(FORMAT)
                print(shutdown_message.decode(FORMAT))
                broadcast(shutdown_message)
                shutdown(client)
                break
            else:
                format_message = f"[{get_timestamp()}] {nickname}: {message.decode(FORMAT)}".encode(FORMAT)
                print(format_message.decode(FORMAT))
                broadcast(format_message)
        except Exception as e:
            print(f"Error handling message: {e}")
            format_message = f"[{get_timestamp()}] {nickname} has disconnected.".encode(FORMAT)
            print(format_message.decode(FORMAT))
            broadcast(format_message)
            shutdown(client)
            break

def receive():
    while is_running:
        try:
            # Accept new Connections
            client, address = server.accept()

            # Request and store Nicknames
            client.send('<NICK>'.encode(FORMAT))
            nickname = client.recv(1024).decode(FORMAT)

            with lock:
                nicknames.append(nickname)
                clients.append(client)

            # Print connection to console
            print(f"{nickname} joined from {str(address[0])}:{str(address[1])}")

            broadcast(f"{nickname} has joined the chat!".encode(FORMAT))
            client.send(f"Successfully connected to the server!".encode(FORMAT))

            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
        except Exception as e:
            print(f"Error receiving connection: {e}")

if __name__ == "__main__":
    try:
        receive()
    except KeyboardInterrupt:
        print("Server is shutting down...")
        is_running = False
        server.close()
