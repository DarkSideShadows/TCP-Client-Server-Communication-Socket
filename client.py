import socket  # Import socket module for network communication

# Constants
HEADER = 64  # Fixed 64-byte header for message length
PORT = 5050  # The same port number used by the server
SERVER = "127.0.0.1"  # Localhost - ensures client connects to a local server
ADDR = (SERVER, PORT)  # Server address tuple (IP, Port)
FORMAT = 'utf-8'  # Encoding format for sending/receiving data
DISCONNECT_MESSAGE = "!DISCONNECT"  # Special message to terminate connection
MAX_MESSAGE_LENGTH = 256  # Maximum length allowed for messages

# Create a client socket using IPv4 (AF_INET) and TCP (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    client.connect(ADDR)  # Connect to the local server
except Exception as e:
    print(f"[ERROR] Could not connect to server: {e}")
    exit()  # Exit if the server is unreachable

def send(msg): # Send method
    
    try:
        if len(msg) > MAX_MESSAGE_LENGTH:
            print("[ERROR] Message too long! Max length is 256 characters.")
            return  # Don't send messages that exceed the limit

        message = msg.encode(FORMAT) # Convert message to bytes
        msg_length = str(len(message)).encode(FORMAT) # Convert message length to a string and encode it
        msg_length += b" " * (HEADER - len(msg_length)) # Pad the message length to be exactly 64 bytes (HEADER size)

        # Send the message length first, then the actual message
        client.send(msg_length)
        client.send(message)

        # Receive and print the response from the server
        response = client.recv(2048).decode(FORMAT)
        print(f"[SERVER RESPONSE] {response}")
    
    # Error Handling
    except (ConnectionResetError, BrokenPipeError):
        print("[ERROR] Connection to server lost.")
        client.close()
        exit()

# Display instructions for the user
print("\n==== CLIENT INSTRUCTIONS ====")
print("1. Type a message to send to the server for encoding.")
print("2. Type 'exit' to disconnect.\n")

# Main loop for user input
while True:
    user_input = input("Enter message (or 'exit' to disconnect): ")

    if user_input.lower() == "exit":
        send(DISCONNECT_MESSAGE)  # Inform the server of disconnection
        break  # Exit the loop and close the connection
    else:
        send(user_input)  # Send the user input to the server for encoding

client.close()  # Close the connection when done
