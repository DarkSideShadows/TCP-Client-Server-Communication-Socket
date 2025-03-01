import socket
import threading  # For handling multiple client connections concurrently

# Constants
HEADER = 64  # First 64 bytes determine the length of the message
PORT = 5050  # Port number where the server will listen for connections
SERVER = "127.0.0.1"  # Localhost - ensures server runs only on the local machine
ADDR = (SERVER, PORT)  # Server address tuple (IP, Port)
FORMAT = 'utf-8'  # Encoding format for sending/receiving data
DISCONNECT_MESSAGE = "!DISCONNECT"  # Special message for clients to disconnect
MAX_MESSAGE_LENGTH = 256  # Maximum allowed message length

# Create a server socket using IPv4 (AF_INET) and TCP (SOCK_STREAM)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)  # Bind the server to the specified IP and port

def encode_message(message):
    #Encodes a message by shifting each character to the next ASCII character
    return ''.join(chr(ord(char) + 1) for char in message)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    try:
        while True:
            # Receive the message length first (fixed 64-byte header)
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if not msg_length:
                break  # No data received, client likely disconnected

            msg_length = int(msg_length)  # Convert length string to integer

            # Ensure the message does not exceed the allowed limit
            if msg_length > MAX_MESSAGE_LENGTH:
                conn.send("Error: Message too long!".encode(FORMAT))
                continue

            # Receive the actual message from the client
            msg = conn.recv(msg_length).decode(FORMAT)

            # Check if the client wants to disconnect
            if msg == DISCONNECT_MESSAGE:
                print(f"[{addr}] Disconnected.")
                break  # Exit the loop and close the connection

            # Encode the received message
            encoded_msg = encode_message(msg)
            print(f"[{addr}] {msg} -> {encoded_msg}")  # Log original and encoded messages

            # Send the encoded message back to the client
            conn.send(encoded_msg.encode(FORMAT))

    except (ConnectionResetError, BrokenPipeError):
        print(f"[ERROR] Connection lost with {addr}.")  # Handle unexpected client disconnections
    
    finally:
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 2}")  # Exclude main thread and current thread
        conn.close()  # Ensure connection is properly closed when done

def start():
    """
    Starts the server and listens for client connections.
    """
    
    server.listen()  # Put the server in listening mode
    print(f"[LISTENING] Server is listening on {SERVER}:{PORT}")

    while True:
        try:
            # Accept incoming client connection
            conn, addr = server.accept()  # conn = socket object, addr = (client_ip, client_port)

            # Start a new thread to handle the client
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()

            # Print the number of active client connections
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")  # Exclude main thread

        except Exception as e:
            print(f"[ERROR] Server encountered an error: {e}")

# Start the server
print("[STARTING] Server is starting...")
start()
