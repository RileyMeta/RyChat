import socket
import threading

is_running = True

stop_event = threading.Event()

HOST, PORT = '127.0.0.1', 55550
FORMAT = 'utf-8'

nickname = input("Choose a nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def receive():
    while not stop_event.is_set():
        try:
            message = client.recv(1024).decode(FORMAT)
            if message == "<NICK>":
                client.send(nickname.encode(FORMAT))
            else:
                print(message)
        except ConnectionResetError:
            print("Connection closed by the server.")
            shutdown()
            break
        except Exception as e:
            print(f"Error receiving message: {e}")
            shutdown()
            break

def write():
    while not stop_event.is_set():
        try:
            message = input("")
            client.send(message.encode(FORMAT))
            if message == '/quit':
                shutdown()
                break
        except Exception as e:
            print(f"Error sending message: {e}")
            break

def shutdown():
    global stop_event, receive_thread, write_thread
    stop_event.set()
    
    client.close()

    if receive_thread.is_alive():
        receive_thread.join()

    print("Client has shut down.")

if __name__ == '__main__':
    receive_thread = threading.Thread(target=receive)
    receive_thread.start()
    write()
