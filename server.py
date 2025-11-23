import socket
import threading
import datetime
import json

# Server Configuration
HOST: str = "0.0.0.0"
PORT: int = 5555
MAX_CLIENTS: int = 12

# List to keep track of connected clients
clients: list[socket.socket] = []
nicknames: list[str] = []


def broadcast(message, sender_socket: socket.socket = None) -> None:
    """
    Sends a message to all connected clients.
    """
    for client in clients:
        # Optional: Don't send back to sender if desired, but usually chat apps show your own msg confirmed
        # For this simple implementation, we send to everyone so they see the server time etc.
        try:
            client.send(message)
        except:
            # If sending fails, remove the client
            remove_client(client)


def remove_client(client: socket.socket) -> None:
    """
    Removes a client from the lists and closes the connection.
    """
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        client.close()
        nickname = nicknames[index]
        nicknames.remove(nickname)

        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        msg = json.dumps(
            {
                "type": "system",
                "content": f"{nickname} left the chat!",
                "timestamp": timestamp,
            }
        )
        broadcast(msg.encode("utf-8"))
        print(f"Client {nickname} disconnected.")


def handle_client(client: socket.socket) -> None:
    """
    Handles a single client connection.
    """
    while True:
        try:
            # Receive message from client
            # Client sends JSON bytes now
            message = client.recv(1024)
            if not message:
                remove_client(client)
                break

            # Broadcast message (it's already JSON bytes from client)
            broadcast(message)
        except:
            remove_client(client)
            break


def receive() -> None:
    """
    Main loop to accept new connections.
    """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((HOST, PORT))
        server.listen(MAX_CLIENTS)
        print(f"Server running on {HOST}:{PORT}")
    except Exception as e:
        print(f"Could not bind to {HOST}:{PORT}. Error: {e}")
        return

    while True:
        try:
            client, address = server.accept()
            print(f"Connected with {str(address)}")

            # Request Nickname
            client.send("<<NICK>>".encode("utf-8"))
            nickname = client.recv(1024).decode("utf-8")

            nicknames.append(nickname)
            clients.append(client)

            print(f"Nickname of the client is {nickname}")

            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            join_msg = json.dumps(
                {
                    "type": "system",
                    "content": f"{nickname} joined the chat!",
                    "timestamp": timestamp,
                }
            )
            broadcast(join_msg.encode("utf-8"))

            welcome_msg = json.dumps(
                {
                    "type": "system",
                    "content": "Connected to the server!",
                    "timestamp": timestamp,
                }
            )
            client.send(welcome_msg.encode("utf-8"))

            # Start handling thread for client
            thread = threading.Thread(target=handle_client, args=(client,))
            thread.start()
        except KeyboardInterrupt:
            print("Server stopping...")
            server.close()
            break
        except Exception as e:
            print(f"Error accepting connection: {e}")


if __name__ == "__main__":
    receive()
