import socket
import threading

user = input("Enter an name: ")
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 59000))

lock = threading.Lock()

def client_recieve():
    while True:
        try:
            message = client.recv(1024).decode("utf-8") # waiting to recieve msg from the server
            lock.acquire()
            if message == "?user":
                client.send(user.encode("utf-8"))
            else:
                print(message)
            lock.release()
        except:
            client.close()
            break

def client_send():
    while True:
        message = input("") # waiting to get the input
        lock.acquire()
        client.send(f"{user}: {message}".encode("utf-8"))
        lock.release()

recieve_thread = threading.Thread(target=client_recieve)
recieve_thread.start()

send_thread = threading.Thread(target=client_send)
send_thread.start()



