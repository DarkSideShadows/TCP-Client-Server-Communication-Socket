import socket
#import pickle # serialize object (pickle), send through socket to server, server unpickles and uses object

# constants
HEADER = 64 # 64 bytes to determine length of message
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # local ip address
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE ="!DISCONNECT" # for clean disconnects (concern: false positive user is connected)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # setup socket for client
client.connect(ADDR) # connect to server

# different send formats: json string? pickle?
def send(obj):
    pass

def send(msg): # send a string
    message = msg.encode(FORMAT) # encode string into a byte object to send through socket
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT) 
    send_length += b" " * (HEADER - len(send_length)) # pad message to get 64 bytes
    client.send(send_length)
    client.send(message)
    print(client.recv(2048).decode(FORMAT)) # handle whatever message is sent back from server

# User input loop for continuous messaging
while True:
    msg = input("Enter message (or type 'exit' to disconnect): ")
    
    if msg.lower() == "exit":
        send(DISCONNECT_MESSAGE)
        break  
    
    send(msg)  

# Close the connection
client.close()
