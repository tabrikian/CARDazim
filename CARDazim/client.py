import argparse
import sys
from Connection import Connection
from Card import Card


def send_data(server_ip: str, server_port: int, data: bytes) -> None:
    """
    Connect to server and send him a message
    :param server_ip: the ip of the server
    :param server_port: the port of the server
    :param data: the message we want to send
    :return: None
    """
    with Connection(host=server_ip, port=server_port) as connection:
        connection.send_message(data)


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('IP', type=str,
                        help='IP of the server')
    parser.add_argument('port', type=int,
                        help='port of connection')

    parser.add_argument('name', type=str,
                        help='name of card')
    parser.add_argument('creator', type=str,
                        help='name of the card\'s creator')
    parser.add_argument('path', type=str,
                        help='path to the image')
    parser.add_argument('riddle', type=str,
                        help='create a riddle to the server')
    parser.add_argument('solution', type=str,
                        help='solution of the riddle')
    return parser.parse_args()


def main():
    """
    Implementation of CLI and sending data to server.
    """
    args = get_args()
    try:
        print("creates card")
        card = Card.create_from_path(args.name, args.creator, args.path, args.riddle, args.solution)
        print("encrypting")
        card.encrypt(args.solution)
        print("sending")
        send_data(args.IP, args.port, card.serialize())
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
