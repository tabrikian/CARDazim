import argparse
import sys
import socket
import time


###########################################################
####################### YOUR CODE #########################
###########################################################


def send_data(server_ip: str, server_port: int, data: str) -> None:
    """
    Connect to server and send him a message
    :param server_ip: the ip of the server
    :param server_port: the port of the server
    :param data: the message we want to send
    :return: None
    """
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, server_port))

    client.send(data.encode())

    client.close()


###########################################################
##################### END OF YOUR CODE ####################
###########################################################


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    parser.add_argument('data', type=str,
                        help='the data')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
    args = get_args()
    try:
        print("sending messages")
        send_data(args.server_ip, args.server_port, args.data)
        print('Done.')
    except Exception as error:
        print(f'ERROR: {error}')
        return 1


if __name__ == '__main__':
    sys.exit(main())
