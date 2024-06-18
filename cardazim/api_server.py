import argparse
import sys

from flask import Flask, request, jsonify
from saver import Saver

# instance of flask application
app = Flask(__name__)


@app.route('/creators', methods=['GET'])
def get_creators():
    if request.method == 'GET':
        data = saver.get_creators()

        return jsonify(data)


@app.route('/creators/<creator>/cards/unsolved', methods=['GET'])
def get_creator_unsolved(creator):
    if request.method == 'GET':
        data = saver.get_creator_unsolved_cards(creator)

        return jsonify(data)


@app.route('/creators/<creator>/cards/solved', methods=['GET'])
def get_creator_solved(creator):
    if request.method == 'GET':
        data = saver.get_creator_solved_cards(creator)

        return jsonify(data)


@app.route('/creators/<creator>/cards/<card_name>', methods=['GET'])
def get_card(creator: str, card_name: str):
    if request.method == 'GET':
        data = saver.get_metadata(card_name, creator)
        return jsonify(data)


@app.route('/creators/<creator>/cards/<card_name>/image.jpg', methods=['GET'])
def get_image(creator: str, card_name: str):
    if request.method == 'GET':
        data = saver.load(saver.get_id_by_name(card_name, creator)).image.image
        return jsonify(data)


@app.route('/cards/find', methods=['GET'])
def find_card(find=""):
    if request.method == 'GET':
        data = saver.get_for_find(find)
        return jsonify(data)


@app.route('/creators/<card_id>/solve', methods=['POST'])
def solve_card(card_id: str, solution: str):
    if request.method == 'POST':
        creator, card_name = saver.get_name_by_id()
        card = saver.load(card_id)
        solved = card.image.decrypt(solution)
        if solved:
            saver.solve_card(card_name, creator, solution)
        return solved


def run_server(server_ip: str, port: int):
    app.run(server_ip, port, debug=True)


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
    global path, saver
    args = get_args()
    path = args.path
    saver = Saver(path)
    run_server(args.server_ip, args.server_port)


if __name__ == '__main__':
    global saver, path
    sys.exit(main())
