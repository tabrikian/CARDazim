import argparse
import sys
import socket
import threading


"""
:param server_ip: the IP of the server
:param server_port: the port
:return: None
"""


def run_server(server_ip: str, server_port: int) -> None:
    """ create the server """
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(5)
    """ 
    The server is up and running
    
    Now handel clients
    """
    while True:
        conn, addr = server.accept()
        t = threading.Thread(target=handel_client, args=[conn, addr])
        t.start()
        print("client connected")


def handel_client(conn: socket, addr: socket) -> None:
    from_client = ''
    while True:
        data = conn.recv(4096)
        if not data: break
        from_client += data.decode('utf8')
        print(f'Received data: {from_client}')
    conn.close()


def get_args():
    parser = argparse.ArgumentParser(description='Send data to server.')
    parser.add_argument('server_ip', type=str,
                        help='the server\'s ip')
    parser.add_argument('server_port', type=int,
                        help='the server\'s port')
    return parser.parse_args()


def main():
    '''
    Implementation of CLI and sending data to server.
    '''
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
