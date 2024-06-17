from CryptImage import CryptImage


class Card:
    def __init__(self, name: str, creator: str, image: CryptImage, riddle: str, solution: str = None) -> None:
        self.name = name
        self.creator = creator
        self.image: CryptImage = image
        self.riddle = riddle
        self.solution = solution

    def __repr__(self) -> str:
        return f"<Card name={self.name}, creator={self.creator}>"

    def __str__(self) -> str:
        solution = self.solution
        if solution is None:
            solution = "unsolved"
        return f"Card {self.name} by {self.creator}\nriddle: {self.riddle}\nsolution: {solution}"

    @staticmethod
    def create_from_path(name: str, creator: str, path: str, riddle: str, solution: str):
        img = CryptImage.create_from_path(path)
        return Card(name, creator, img, riddle, solution)

    def serialize(self) -> bytes:
        image_data = CryptImage.image_to_bytes(self.image)

        key_hash = self.image.key_hash
        if key_hash is None:
            key_hash = int(0).to_bytes(32, "big")

        return (len(self.name).to_bytes(4, "big") + self.name.encode() +
                len(self.creator).to_bytes(4, "big") + self.creator.encode() +
                self.image.length.to_bytes(4, "big") + self.image.height.to_bytes(4, "big") + image_data +
                key_hash + len(self.riddle).to_bytes(4, "big") + self.riddle.encode())

    def encrypt(self, key: str) -> None:
        self.image.encrypt(key)

    def decrypt(self, key: str) -> bool:
        return self.image.decrypt(key)

    @staticmethod
    def deserialize(data: bytes) -> "Card":
        len_name = int.from_bytes(data[:4], "big")
        data = data[4:]
        name = data[:len_name].decode()
        data = data[len_name:]

        len_creator = int.from_bytes(data[:4], "big")
        data = data[4:]
        creator = data[:len_creator].decode()
        data = data[len_creator:]

        length = int.from_bytes(data[:4], "big")
        data = data[4:]
        height = int.from_bytes(data[:4], "big")
        data = data[4:]

        image_data = data[:length * height * 3 + 32]
        data = data[length * height * 3 + 32:]

        len_riddle = int.from_bytes(data[:4], "big")
        data = data[4:]
        riddle = data[:len_riddle].decode()

        return Card(name, creator, CryptImage.bytes_to_image(image_data, length, height), riddle)


def test():
    solution = "HA HA!"
    card = Card.create_from_path("card", "Omri", "/home/user/Pictures/panda.jpg",
                                 "what?", solution)
    card.image.encrypt(card.solution)
    card.image.image.show()
    data = card.serialize()
    card2 = Card.deserialize(data)
    if card2.image.decrypt(solution):
        card2.solution = solution
    assert (repr(card) == repr(card2))
