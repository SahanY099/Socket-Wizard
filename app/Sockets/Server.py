import socket
import threading

class Server:
    def __init__(self, port: int, connections: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.maximum_connections = connections
        self.list_of_clients = []
        self.print_lock = threading.Lock()

    def client_thread(self, conn: socket.socket, addr: tuple) -> None:
        conn.send("Welcome to this chatroom!".encode())

        while True:
            try:
                message = conn.recv(2048).decode()
                if message:
                    print("<" + addr[0] + "> " + message)
                    self.broadcast(message, conn)
                    message_to_send = input("->")
                    self.broadcast(message_to_send,conn)
                    conn.send(message_to_send.encode())

                else:
                    self.remove(conn)

            except Exception as ex:
                print(ex)
                break

    def broadcast(self, message: str, connection: socket.socket) -> None:
        with self.print_lock:
            for client in self.list_of_clients:
                if client != connection:
                    try:
                        client.send(message.encode())
                    except Exception:
                        client.close()
                        self.remove(client)

    def remove(self, connection: socket.socket) -> None:
        if connection in self.list_of_clients:
            self.list_of_clients.remove(connection)

    def start_server(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(self.maximum_connections)
            print(f"Host: {self.host}\t Port: {self.port}\t Maximum Connection: {self.maximum_connections}")
            print("Server started.")

            while True:
                conn, addr = self.server_socket.accept()
                self.list_of_clients.append(conn)
                print(addr[0] + " connected")
                threading.Thread(target=self.client_thread, args=(conn, addr)).start()

        except Exception as ex:
            print(ex)
            print("Failed to establish connection.")

        finally:
            for conn in self.list_of_clients:
                conn.close()

            self.server_socket.close()

