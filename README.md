# TCP Client-Server Project
Group 9's submission for programming assignment 1 in Dr. Wang's CS576 @ SDSU


---

## **Features**
- Implements **local TCP communication** using `127.0.0.1:5050`  
- **Encodes** messages sent from the client  
- Supports **multiple clients** using Python's `threading` module  
- **Graceful disconnect handling**  
- **Error handling** for invalid input and unexpected connection losses  

---

## **Requirements**
- Python 3.x installed
- Runs **locally** on `127.0.0.1`
- No additional dependencies required

---


---

## **How to Run the Program**
### **Step 1: Start the Server**
Open a terminal and run:
```sh
python server.py
```
Expected output:
```
[STARTING] Server is starting...
[LISTENING] Server is listening on 127.0.0.1:5050
```

### **Step 2: Start the Client**
Open another terminal and run:
```sh
python client.py
```
Expected output:
```
==== CLIENT INSTRUCTIONS ====
1. Type a message to send to the server for encoding.
2. Type 'exit' to disconnect.

Enter message (or 'exit' to disconnect): Hello
[SERVER RESPONSE] Ifmmp
```

### **Step 3: Send Messages**
Try different inputs:
```
Enter message (or 'exit' to disconnect): Goodbye
[SERVER RESPONSE] Hppebzf
```

### **Step 4: Disconnect**
To disconnect, type:
```
Enter message (or 'exit' to disconnect): exit
```
The client will close, and the server logs:
```
[NEW CONNECTION] ('127.0.0.1', 52509) connected.
[Goodbye]
[52509] Disconnected.
```

---
## **Code Breakdown**
### **server.py**
- **Creates a TCP socket**
- **Encodes messages** using ASCII shifting (`chr(ord(char) + 1)`)
- **Handles multiple clients** using `threading`
- **Closes connections gracefully**

### **client.py**
- **Connects to the local server**
- **Sends messages** and receives encoded responses
- **Handles errors and disconnections properly**

---

## Credits  
This project was built with guidance from the following tutorial:  
[Python Socket Programming Tutorial](https://www.youtube.com/watch?v=3QiPPX-KeSc) by Tech With Tim.
