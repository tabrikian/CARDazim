import os

import pymongo

from typing import List
from Card import Card
from database import DataBase


class Saver(DataBase):
    def __init__(self, mongo_url: str, image_saver: str = "./images"):
        client = pymongo.MongoClient(mongo_url)
        db = client['cardazim']
        self.collection = db["cards"]
        print("hi")
        print(db.list_collection_names())
        self.image_saver = image_saver
        if not os.path.exists(image_saver):
            os.makedirs(image_saver)

    def get_identifier(self, card: Card) -> str:
        return card.creator + "--" + card.name

    def get_id_by_name(self, name, creator):
        return creator + "--" + name

    def get_name_by_id(self, id_: str):
        return tuple(id_.split("--"))

    def save(self, card):
        print("saving...")
        path = f"{self.image_saver}/{self.get_id_by_name(card.name, card.creator)}.jpg"
        card.image.image.save(path)
        data = {"name": card.name, "creator": card.creator, "riddle": card.riddle, "solution": card.solution,
                "path": path, "id": self.get_id_by_name(card.name, card.creator)}
        self.collection.insert_one(data)
        print("saved")

    def load(self, identifier: str):
        name, creator = self.get_name_by_id(identifier)
        myquery = {"creator": creator, "name": name}
        cards_of_creators = self.collection.find(myquery)
        cards = [Card.create_from_path(card["name"], card["creator"], card["path"], card["riddle"], card["solution"])
                 for card in cards_of_creators]
        return cards[0]

    def get_creators(self) -> List[str]:
        return list({card["creator"] for card in self.collection.find()})

    def get_creator_cards(self, creator):
        myquery = {"creator": creator}
        cards_of_creators = self.collection.find(myquery)
        cards = [Card.create_from_path(card["name"], card["creator"], card["path"], card["riddle"], card["solution"])
                 for card in cards_of_creators]
        return cards

    def get_creator_unsolved_cards(self, creator):
        myquery = {"creator": creator, "solution": None}
        cards_of_creators = self.collection.find(myquery)
        return list({card["name"] for card in cards_of_creators})

    def get_creator_solved_cards(self, creator):
        myquery = {"creator": creator, "solution": {"$ne": None}}
        cards_of_creators = self.collection.find(myquery)
        return list({card["name"] for card in cards_of_creators})

    def solve_card(self, name: str, creator: str, solution: str):
        myquery = {"creator": creator, "name": name}
        new_values = {"$set": {"solution": solution}}
        self.collection.update_one(myquery, new_values)

    def get_metadata(self, name: str, creator: str):
        myquery = {"creator": creator, "name": name}
        cards_of_creators = self.collection.find(myquery)
        cards = [{"name": card["name"], "creator": card["creator"], "path": card["path"], "riddle": card["riddle"], "solution": card["solution"]}
                 for card in cards_of_creators]
        return cards[0]

    def get_for_find(self, find):
        cards_of_creators = self.collection.find()
        cards = [{"name": card["name"], "creator": card["creator"], "path": card["path"], "riddle": card["riddle"],
                  "solution": card["solution"]}
                 for card in cards_of_creators if find in card["name"]]
        return cards
