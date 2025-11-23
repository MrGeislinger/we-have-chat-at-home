# Local Chat Server

I have implemented a simple, robust local chat server and client using Python's standard `socket` and `threading` libraries.

## Features

### Server
- Listens on `0.0.0.0:5555`.
- Handles multiple clients using threads.
- Broadcasts messages as JSON objects.
- Manages nicknames and disconnections.

### Client
- Connects to the server.
- Uses two threads: one for listening to incoming messages and one for sending user input.
- Sends and receives messages as JSON objects.
- Uses `rich` to color-code usernames and highlight system messages.
- **TTS Feature:** If run with `say` argument (e.g., `python3 client.py <IP> 5555 say`), it reads messages aloud.
  - Only reads messages from other users.
  - **Configurable Settings:** Use the `/speak` command to pass any flags to the system `say` command.
    - `/speak -v Alex` (Set voice to Alex)
    - `/speak -r 200` (Set rate to 200 words/min)
    - `/speak -v Samantha -r 180` (Set both)
    - `/speak -v=Fred` (Alternative syntax)
    - `/speak v=Fred` (Alternative syntax)
    - `/speak v Fred` (Alternative syntax)
    - `/speak voice Fred` (Alternative syntax)
  - **Removing Settings:** Use `key=` (empty value), `key=""`, or `key=''` to remove a setting.
    - `/speak -v=` (Removes voice setting)
    - `/speak -r ""` (Removes rate setting)
    - `/speak -r ''` (Removes rate setting)
- Supports a `/quit` command to exit gracefully.

## How to Run

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Server (on Ubuntu machine):**
   ```bash
   python3 server.py
   ```
   *Note the IP address of this machine (e.g., using `ifconfig` or `ip a`).*

3. **Start a Client (on Mac or Linux):**
   ```bash
   python3 client.py <SERVER_IP> 5555 [say]
   ```
   *Replace `<SERVER_IP>` with the actual IP address of the server.*
   *Add `say` at the end to enable Text-to-Speech.*

4. **Chat:**
   - Enter your nickname when prompted.
   - Type messages and press Enter to send.
   - Type `/quit` to leave.
