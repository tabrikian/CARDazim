import socket


close_exception = Exception("connection closed")

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
        len_mess = len(message)
        self.conn.send(len_mess.to_bytes(32, "big") + message)

    def receive_message(self) -> bytes:
        len_mess = int.from_bytes(self.conn.recv(32), "big")
        data = int(1).to_bytes(1, "big")
        while len_mess > len(data):
            data += self.conn.recv(min(len_mess - len(data), 4096))
        data = data[1:]
        if not data:
            raise close_exception
        return data

    def connect(self, host: str, port: int):
        self.conn.connect((host, port))

    def close(self):
        self.conn.close()
