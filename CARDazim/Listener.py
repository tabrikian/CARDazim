import socket
from Connection import Connection


class Listener:
    def __init__(self, host: str, port: int, backlog: int = 1000):
        self.host = host
        self.port = port
        self.backlog = backlog
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.start()

    def __repr__(self) -> str:
        return "Listener(port=" + str(self.port) + ", host=" + self.host + ", backlog=" + str(self.backlog) + ")"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def start(self):
        self.conn.bind((self.host, self.port))
        self.conn.listen(5)

    def stop(self):
        self.conn.close()

    def accept(self):
        conn, addr = self.conn.accept()
        return Connection(conn)
