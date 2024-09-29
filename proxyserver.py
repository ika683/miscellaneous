import socket
import threading

class Proxy:
    def __init__(self, host='127.0.0.1', port=8080):
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(5)
        print(f'Listening on {self.host}:{self.port}...')

    def handle_client(self, client_socket):
        request = client_socket.recv(1024)
        print(f'Request: {request.decode()}')

        # Parse the HTTP request
        lines = request.decode().splitlines()
        if lines:
            # Extract the first line to get the URL
            method, url, _ = lines[0].split()

            # Strip the http:// or https://
            url = url.split("://")[-1]
            host, port = (url.split(":") + [80])[:2]

            # Create a socket to the destination server
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.connect((host, int(port)))

            # Forward the request to the actual server
            server_socket.send(request)

            # Receive the response from the server
            while True:
                response = server_socket.recv(4096)
                if len(response) == 0:
                    break
                client_socket.send(response)

            server_socket.close()
        client_socket.close()

    def start(self):
        while True:
            client_socket, addr = self.server.accept()
            print(f'Accepted connection from {addr}')
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.start()
if __name__ == "__main__":
    proxy = Proxy()
    proxy.start()
