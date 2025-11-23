import socket
import threading
import time
import sys
import json
import datetime

def listen_for_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received: {message}")
        except:
            break

def mock_client(name, messages):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5555))
        
        # Handle nickname request
        msg = client.recv(1024).decode('utf-8')
        if msg == 'NICK':
            client.send(name.encode('utf-8'))
        
        # Start listening thread
        listener = threading.Thread(target=listen_for_messages, args=(client,))
        listener.daemon = True
        listener.start()
        
        # Wait for connection confirmation
        time.sleep(0.5)
        
        for message in messages:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            msg_dict = {
                "type": "message",
                "sender": name,
                "content": message,
                "timestamp": timestamp
            }
            client.send(json.dumps(msg_dict).encode('utf-8'))
            time.sleep(0.1)
            
        time.sleep(1) # Wait for messages to be received
        client.close()
    except Exception as e:
        print(f"Client {name} error: {e}")

if __name__ == "__main__":
    print("Starting test clients...")
    t1 = threading.Thread(target=mock_client, args=("Alice", ["Hello from Alice"]))
    t2 = threading.Thread(target=mock_client, args=("Bob", ["Hello from Bob"]))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
    print("Test clients finished.")
