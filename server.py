import socket
import threading

host = "127.0.0.1"
port = 59000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = {} # key = username, value = client socket object

# sending a message to all clients from server
def broadcoast(message):
    for user in clients:
        client = clients[user]
        client.send(message.encode("utf-8"))

# handle connections of clients
def handle_room(user):
    while True:
        try:
            client = clients[user]
            message = client.recv(1024).decode("utf-8") # recieving data in a buffer size of 1024
            broadcoast(message)
        except:
            del clients[user]
            client.close()
            broadcoast(f"{user} has left the chat room.")

if __name__ == "__main__":
    print("Server is runnin and listening...\n")
    while True:
        client, address = server.accept()
        print(f"\tConnection established with {str(address)}")
        
        client.send(b"?user")
        user = client.recv(1024).decode("utf-8")
        clients[user] = client
        
        print(f"\tThe name of the client is {user}")
        broadcoast(f"{user} has entered the chat room.")

        client_thread = threading.Thread(target=handle_room, args=(user,))
        client_thread.start()

        print("\n")