import socket
import threading

# constants
HEADER = 64 # 64 bytes to determine length of message
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname()) # local ip address
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE ="!DISCONNECT" # for clean disconnects (concern: false positive user is connected)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # open device to other connections, send data through stream
server.bind(ADDR) # anything that connects to this server goes to ADDR

def encode_message(message):
    return ''.join(chr(ord(char) + 1) for char in message)

# Handle individual client connections
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:  # Check for a valid message
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == DISCONNECT_MESSAGE:
                connected = False  # Disconnect if user sends "!DISCONNECT"

            print(f"[{addr}] {msg}")

            # send message from server to client
            encoded_msg = encode_message(msg)
            conn.send(encoded_msg.encode(FORMAT))

    conn.close()  # Close the connection

def start():
   server.listen() # listen to connections
   print(f"[LISTENING] Server is listening on {SERVER}")
   while True: 
       # wait for new connection
       # information: ip addr, port (addr) & connection object (conn)
       conn, addr = server.accept() 
       thread = threading.Thread(target=handle_client, args=(conn, addr))
       thread.start()
       print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

print("[STARTING] server is starting...")
start()
