import socket
import argparse

def main():
    parser = argparse.ArgumentParser(description="Chatbot Client")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="Server IP address")
    parser.add_argument("--port", type=int, default=5555, help="Server port")
    args = parser.parse_args()

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((args.host, args.port))
    print("Connected to the server. Type 'exit' to quit.")

    while True:
        message = input("You: ")
        if message.lower() == "exit":
            break
        client.send(message.encode())
        response = client.recv(1024).decode()
        print(f"Server: {response}")

    client.close()

if __name__ == "__main__":
    main()