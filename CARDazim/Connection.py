import socket


class Connection:
    def __init__(self, connection: socket.socket = None, host: str = None, port: int = -1):
        self.conn = connection
        if self.conn is None:
            self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if host is not None and port > -1:
            self.connect(host, port)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def __repr__(self) -> str:
        return "<Connection from " + socket.gethostname() + " to " + self.conn.getpeername() + ">"

    def send_message(self, message: bytes):
        self.conn.send(message)

    def receive_message(self) -> str:
        data = self.conn.recv(4096)
        if not data:
            raise "connection closed"
        from_connection = data.decode('utf8')
        return from_connection

    def connect(self, host: str, port: int):
        self.conn.connect((host, port))

    def close(self):
        self.conn.close()
