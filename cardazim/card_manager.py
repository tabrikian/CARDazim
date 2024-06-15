import json
import os
import shutil

from typing import List
from Card import Card
from database import DataBase


class CardManager(DataBase):
    def __init__(self, dir_path: str = '.'):
        self.paths_by_id = {}
        self.dir_path = dir_path
        if os.path. exists(self.dir_path):
            shutil. rmtree(self.dir_path)

    def save(self, card: Card):
        id = self.get_identifier(card)
        database_path = self.dir_path
        if not os.path.exists(database_path):
            os.makedirs(database_path)
            with open(f"{self.dir_path}/creators.txt", "x"):
                pass

        creator_path = f"{self.dir_path}/{card.creator}"
        if not os.path.exists(creator_path):
            os.makedirs(creator_path)
            with open(f"{creator_path}/cards.txt", "x"):
                pass
            with open(f"{self.dir_path}/creators.txt", "a") as file:
                file.write(card.creator + "\n")

        card_path = f"{creator_path}/{card.name}"
        if not os.path.exists(card_path):
            os.makedirs(card_path)
            with open(f"{creator_path}/cards.txt", "a") as file:
                file.write(card.name + "\n")

        with open(f"{card_path}/metadata.json", "x") as file:
            data = {"name": card.name, "creator": card.creator, "riddle": card.riddle, "solution": card.solution,
                    "path": f"{card_path}/image.jpg"}
            file.write(json.dumps(data))

        card.image.image.save(f"{card_path}/image.jpg")
        self.paths_by_id[id] = f"{card_path}"

    def get_identifier(self, card: Card) -> str:
        return card.creator + "--" + card.name

    def get_id_by_name(self, name, creator):
        return creator + "--" + name

    def load(self, identifier: str) -> Card:
        with open(f"{self.paths_by_id[identifier]}/metadata.json", "r") as file:
            data = json.load(file)
        return Card.create_from_path(data["name"], data["creator"], data["path"], data["riddle"], data["solution"])

    def get_creators(self) -> List[str]:
        new_path = f"{self.dir_path}/creators.txt"
        if not os.path.exists(new_path):
            return []
        with open(new_path, "r") as file:
            data = file.read()
        if len(data) > 0 and data[-1] == "\n":
            data = data[:-1]
        return data.split("\n")

    def get_creator_cards(self, creator) -> List[Card]:
        print(self.paths_by_id)
        new_path = f"{self.dir_path}/{creator}/cards.txt"
        if not os.path.exists(new_path):
            return []
        with open(new_path, "r") as file:
            data = file.read()
        if len(data) > 0 and data[-1] == "\n":
            data = data[:-1]
        card_names = data.split("\n")

        cards = []
        for name in card_names:
            cards.append(self.load(self.get_id_by_name(name, creator)))
        return cards
