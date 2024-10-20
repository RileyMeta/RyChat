import socket
import threading

is_running = True

HOST, PORT = '127.0.0.1', 55555
FORMAT = 'utf-8'

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while is_running:
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == "<NICK>":
                client.send(nickname.encode(FORMAT))
            else:
                print(message)
        except:
            print("An Error Occurred.")
            client.close()
            break

def write():
    while is_running:
        message = input("")
        client.send(message.encode(FORMAT))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
