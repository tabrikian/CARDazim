import argparse
import sys

from flask import Flask, request, jsonify, render_template
from saver import Saver

# instance of flask application
app = Flask(__name__)


@app.route('/creators', methods=['GET'])
def home():
    return render_template("home.html",
                           title="cards")


@app.route('/creators', methods=['GET'])
def get_creators():
    if request.method == 'GET':
        data = saver.get_creators()

        return render_template("show_list.html",
                               title="creators",
                               lst=data)


@app.route('/creators/creator/cards/unsolved', methods=['GET'])
def get_creator_unsolved():
    creator = request.args.get("creator")
    if request.method == 'GET':
        data = saver.get_creator_unsolved_cards(creator)

        return render_template("show_list.html",
                               title="unsolved " + creator + "'s cards",
                               lst=data)


@app.route('/creators/creator/cards/solved', methods=['GET'])
def get_creator_solved():
    creator = request.args.get("creator")
    if request.method == 'GET':
        data = saver.get_creator_solved_cards(creator)

        return render_template("show_list.html",
                               title="solved " + creator + "'s cards",
                               lst=data)


@app.route('/creators/<creator>/cards/<card_name>', methods=['GET'])
def get_card():
    creator = request.args.get("creator")
    card_name = request.args.get("card_name")
    if request.method == 'GET':
        data = saver.get_metadata(card_name, creator)

        return render_template("show_list.html",
                               title=card_name + "--" + creator + "'s data",
                               lst=data)


@app.route('/creators/creator/cards/card_name/image.jpg', methods=['GET'])
def get_image():
    creator = request.args.get("creator")
    card_name = request.args.get("card_name")
    if request.method == 'GET':
        data = saver.load(saver.get_id_by_name(card_name, creator)).image.image
        return render_template("image.html",
                               title="image of " + str(creator) + " card " + str(card_name),
                               path=data)


@app.route('/cards/find', methods=['GET'])
def find_card():
    find = request.args.get("find")
    if request.method == 'GET':
        data = saver.get_for_find(find)

        return render_template("show_list.html",
                               title="cards found for " + find,
                               lst=data)


@app.route('/creators/card_id/solve', methods=['POST'])
def solve_card():
    card_id = request.args.get("card_id")
    solution = request.args.get("solution")
    if request.method == 'POST':
        creator, card_name = saver.get_name_by_id()
        card = saver.load(card_id)
        solved = card.image.decrypt(solution)
        if solved:
            saver.solve_card(card_name, creator, solution)

        solve_message = "solution is wrong" if not solved else "solved!!!"

        return render_template("show_list.html",
                               title=solve_message,
                               lst="")


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
