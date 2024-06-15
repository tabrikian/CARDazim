import argparse
import sys
import threading
from Listener import Listener
from Connection import Connection
from Card import Card
from card_manager import CardManager


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
    global saver, path
    with connection as conn:
        try:
            data = conn.receive_message()
        except Exception as error:
            print(f'ERROR: {error}')
        card = Card.deserialize(data)
        print(f'Received card: {card}')
        id = saver.save(card)
        print(f'Card saved in {path}/{id}')


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('path', type=str,
                        help='where to save the cards?')
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    global path, saver
    args = get_args()
    path = args.path
    saver = CardManager(path)
    try:
        print("server is ready")
        run_server(args.server_ip, args.server_port)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    global saver, path
    sys.exit(main())
