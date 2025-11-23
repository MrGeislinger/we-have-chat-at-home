import socket
import threading
import sys
import datetime
import json
import os
import random
from rich.console import Console

console = Console()

COLORS = [
    'red',
    'cyan',
    'magenta',
    'green',
    'yellow',
    'white',
]

def get_color(username, color_list=COLORS):
    """
    Deterministically assigns a color to a username.
    """
    
    hash_val = sum(ord(c) for c in username)
    return color_list[hash_val % len(color_list)]

tts_settings = {}

def speak(message: str) -> None:
    """
    Speaks the message using the system's text-to-speech.
    """
    cmd = "say"
    for flag, value in tts_settings.items():
        # Use single hyphen if one character, double hyphen if multiple characters
        if flag.startswith('-'):
            cmd += f" {flag} {value}"
        elif len(flag) == 1:
            cmd += f" -{flag} {value}"
        else:
            cmd += f" --{flag} {value}"
    
    # Escape double quotes in message
    safe_message = message.replace('"', '\\"')
    cmd += f" \"{safe_message}\""
    os.system(cmd)

def receive_messages(client_socket, speak_enabled: bool = False):
    """
    Listens for messages from the server and prints them.
    """
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == 'NICK':
                client_socket.send(nickname.encode('utf-8'))
            else:
                try:
                    data = json.loads(message)
                    timestamp = data.get('timestamp', '')
                    content = data.get('content', '')
                    
                    if data.get('type') == 'message':
                        sender = data.get('sender', 'Unknown')
                        color = get_color(sender)
                        console.print(f"[{timestamp}] [{color}]{sender}[/{color}]: {content}")
                        if speak_enabled and sender != nickname:
                            say_message = f'{sender} says: {content}'
                            speak(say_message)
                    elif data.get('type') == 'system':
                        console.print(f"[{timestamp}] [bold red][System][/bold red]: {content}")
                    else:
                        console.print(message)
                except json.JSONDecodeError:
                    # Fallback for non-JSON messages (shouldn't happen with new server)
                    console.print(message)
        except Exception as e:
            console.print(f"An error occurred! Disconnecting...\n{e}")
            client_socket.close()
            break

def write_messages(client_socket: socket.socket):
    """
    Reads input from the user and sends it to the server.
    """
    while True:
        try:
            text = input('')
            if text.lower() == '/quit':
                client_socket.close()
                sys.exit()
            elif text.lower().startswith('/speak'):
                # Parse generic flags: /speak -v Alex -r 200 or /speak -v=Alex
                args = text.split()[1:]
                i = 0
                while i < len(args):
                    arg = args[i]
                    if '=' in arg:
                        key, value = arg.split('=', 1)
                        tts_settings[key] = value
                    elif i + 1 < len(args):
                        # Assume next arg is value
                        key = arg
                        value = args[i+1]
                        tts_settings[key] = value
                        i += 1
                    else:
                        # Flag without value? Ignore or store as empty?
                        # 'say' usually requires values for flags like -v, -r.
                        # Let's store it just in case.
                        tts_settings[arg] = ""
                    i += 1
                
                console.print(f"[bold green]TTS Settings updated:[/bold green] {tts_settings}")
                continue

            # Add timestamp and nickname
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            message_dict = {
                "type": "message",
                "sender": nickname,
                "content": text,
                "timestamp": timestamp
            }
            message = json.dumps(message_dict)
            client_socket.send(message.encode('utf-8'))
        except:
            print("Error sending message.")
            client_socket.close()
            break

if __name__ == "__main__":
    match sys.argv:
        case [_, host, port]:
            speak_enabled = False
        case [_, host, port, say]:
            speak_enabled = True
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
    receive_thread = threading.Thread(target=receive_messages, args=(client, speak_enabled))
    receive_thread.start()

    write_thread = threading.Thread(target=write_messages, args=(client,))
    write_thread.start()
