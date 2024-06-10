import argparse
import sys
import threading
from Listener import Listener
from Connection import Connection
from Card import Card


"""
:param server_ip: the IP of the server
:param server_port: the port
:return: None
"""


def run_server(server_ip: str, server_port: int) -> None:
    """ create the server """
    with Listener(server_ip, server_port) as listener:

        while True:
            conn = listener.accept()
            t = threading.Thread(target=handel_client, args=[conn])
            t.start()
            print("client connected")


def handel_client(connection: Connection) -> None:
    with connection as conn:
        while True:
            try:
                data = conn.receive_message()
            except:
                break
            card = Card.deserialize(data)
            print(f'Received card: {card}')


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        print("server is ready")
        run_server(args.server_ip, args.server_port)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
