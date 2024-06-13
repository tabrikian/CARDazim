import json
import os
from Card import Card


class CardManager:
    def __init__(self):
        self.paths_by_id = {}

    def save(self, card: Card, dir_path: str = '.') -> str:
        id = self.get_identifier(card)

        new_path = f"{dir_path}/{id}"
        if not os.path.exists(new_path):
            os.makedirs(new_path)

        with open(f"{new_path}/metadata.json", "x") as file:
            data = {"name": card.name, "creator": card.creator, "riddle": card.riddle, "solution": card.solution,
                    "path": f"{new_path}/image.jpg"}
            file.write(json.dumps(data))

        card.image.image.save(f"{new_path}/image.jpg")
        self.paths_by_id[id] = f"{new_path}"
        return id

    def get_identifier(self, card: Card) -> str:
        return card.name + "--" + card.creator

    def load(self, identifier: str) -> Card:
        with open(f"{self.paths_by_id[identifier]}/{identifier}/metadata.json", "r") as file:
            data = json.load(file)
        return Card.create_from_path(data["name"], data["creator"], data["path"], data["riddle"], data["solution"])
