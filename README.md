# Local Chat Server Walkthrough

I have implemented a simple, robust local chat server and client using Python's standard `socket` and `threading` libraries.

## Changes

### Server
- Created `server.py` which listens on `0.0.0.0:5555`.
- Handles multiple clients using threads.
- Broadcasts messages to all connected clients.
- Manages nicknames and disconnections.

### Client
- Created `client.py` which connects to the server.
- Uses two threads: one for listening to incoming messages and one for sending user input.
- Supports a `/quit` command to exit gracefully.

## Verification Results

### Automated Test
I ran a test script `test_chat.py` that simulated two clients (Alice and Bob) connecting to the server.
**Server Log Output:**
```
Server running on 0.0.0.0:5555
Connected with ('127.0.0.1', 54086)
Nickname of the client is Alice
Connected with ('127.0.0.1', 54087)
Nickname of the client is Bob
Client Bob disconnected.
Client Alice disconnected.
```

## How to Run

1. **Start the Server (on Ubuntu machine):**
   ```bash
   python3 server.py
   ```
   *Note the IP address of this machine (e.g., using `ifconfig` or `ip a`).*

2. **Start a Client (on Mac or Linux):**
   ```bash
   python3 client.py <SERVER_IP> 5555
   ```
   *Replace `<SERVER_IP>` with the actual IP address of the server.*

3. **Chat:**
   - Enter your nickname when prompted.
   - Type messages and press Enter to send.
   - Type `/quit` to leave.
