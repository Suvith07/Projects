import socket
import paramiko
import threading
import os

class SSHServer(paramiko.ServerInterface):
    def __init__(self, log_file):
        self.log_file = log_file
   
    def log_credentials(self, username, password):
        with open(self.log_file, 'a') as f:
            f.write(f"Username: {username}, Password: {password}\n")
   
    def check_auth_password(self, username: str, password: str) -> int:
        print(f"Received credentials - Username: {username}, Password: {password}")
        self.log_credentials(username, password)  # Log credentials to file
        # Always fail for now
        return paramiko.AUTH_FAILED


def handle_connection(client_sock):
    try:
        transport = paramiko.Transport(client_sock)
        # Load server key
        server_key_path = 'key'
        if not os.path.exists(server_key_path):
            # Generate a new key if not present
            print("Server key not found. Generating a new key...")
            server_key = paramiko.RSAKey.generate(2048)
            server_key.write_private_key_file(server_key_path)
        else:
            server_key = paramiko.RSAKey.from_private_key_file(server_key_path)
       
        transport.add_server_key(server_key)
       
        # Initialize SSHServer with the log file path
        log_file = 'credentials.log'
        ssh = SSHServer(log_file)
       
        transport.start_server(server=ssh)

        # Wait for a channel
        channel = transport.accept(20)
        if channel is None:
            print("No channel received")
            return

        print("Client authenticated, channel opened")
        channel.send("Hello, this is the server!\n")
        channel.shutdown_write()
        channel.close()
    except Exception as e:
        print(f"Error handling connection: {e}")
    finally:
        client_sock.close()

def main():
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind(('', 2222))
    server_sock.listen(5)  # Listen for up to 5 connections

    print("Server is listening on port 2222...")

    while True:
        client_sock, client_addr = server_sock.accept()
        print(f"Connection from {client_addr[0]}:{client_addr[1]}")
        t = threading.Thread(target=handle_connection, args=(client_sock,))
        t.start()

if __name__ == "__main__":
    main()
