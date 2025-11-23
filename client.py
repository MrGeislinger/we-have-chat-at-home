import socket
import threading
import sys
import datetime
import os

def receive_messages(client_socket, speak: bool = False):
    """
    Listens for messages from the server and prints them.
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'NICK':
                client_socket.send(nickname.encode('utf-8'))
            else:
                # Always print the message
                print(message)
                if speak:
                    os.system(f"say  \"{message}\"")
        except:
            print("An error occurred! Disconnecting...")
            client_socket.close()
            break

def write_messages(client_socket):
    """
    Reads input from the user and sends it to the server.
    """
    while True:
        try:
            text = input('> ')
            if text.lower() == '/quit':
                client_socket.close()
                sys.exit()
            
            # Add timestamp and nickname
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            message = f"[{timestamp}] {nickname}: {text}"
            client_socket.send(message.encode('utf-8'))
        except:
            print("Error sending message.")
            client_socket.close()
            break

if __name__ == "__main__":
    match sys.argv:
        case [_, host, port]:
            speak = False
        case [_, host, port, say]:
            speak = True
        case _:
            print("Usage: python3 client.py <Server IP> <Port>")
            sys.exit(1)
    
    port = int(port)

    nickname = input("Choose your nickname: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except Exception as e:
        print(f"Could not connect to server at {host}:{port}. Error: {e}")
        sys.exit(1)

    # Start threads for listening and writing
    receive_thread = threading.Thread(
        target=receive_messages, args=(client, speak)
    )
    receive_thread.start()

    write_thread = threading.Thread(target=write_messages, args=(client,))
    write_thread.start()
