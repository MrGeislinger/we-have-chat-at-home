import socket
import threading
import time
import sys

def mock_client(name, messages):
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('127.0.0.1', 5555))
        
        # Handle nickname request
        msg = client.recv(1024).decode('utf-8')
        if msg == 'NICK':
            client.send(name.encode('utf-8'))
        
        # Wait for connection confirmation
        time.sleep(0.5)
        
        for message in messages:
            client.send(message.encode('utf-8'))
            time.sleep(0.1)
            
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
