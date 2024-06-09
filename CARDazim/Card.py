from CryptImage import CryptImage
from PIL import Image


class Card:
    def __init__(self, name: str, creator: str, image: CryptImage, riddle: str, solution: str = None):
        self.name = name
        self.creator = creator
        self.image = image
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
        img = self.image.image.load()
        image_data = int(1).to_bytes(1, "big")
        for i in range(self.image.height):
            print(i, self.image.height)
            for j in range(self.image.length):
                pix = img[j, i]
                for c in range(3):
                    image_data += pix[c].to_bytes(1, "big")
        image_data = image_data[1:]

        key_hash = self.image.key_hash
        if key_hash is None:
            key_hash = int(0).to_bytes(32, "big")

        return (len(self.name).to_bytes(4, "big") + self.name.encode() +
                len(self.creator).to_bytes(4, "big") + self.creator.encode() +
                self.image.length.to_bytes(4, "big") + self.image.height.to_bytes(4, "big") + image_data +
                key_hash + len(self.riddle).to_bytes(4, "big") + self.riddle.encode())

    @staticmethod
    def deserialize(data: bytes):
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
        image_data = data[:length*height*3]
        data = data[length*height*3:]
        print(len(data))
        print(length, height)

        counter = 0
        image_rgb = []
        for i in range(length):
            for j in range(height):
                color = [0, 0, 0]
                for c in range(3):
                    color[c] = image_data[counter]
                    counter += 1
                image_rgb.append(tuple(color))
        image_rgb = tuple(image_rgb)

        image = Image.new("RGB", (length, height))
        image.putdata(image_rgb)

        hash_key = data[:32]
        data = data[32:]

        len_riddle = int.from_bytes(data[:4], "big")
        data = data[4:]
        riddle = data[:len_riddle].decode()

        return Card(name, creator, CryptImage(image, hash_key), riddle)


if __name__ == "__main__":
    solution = "HA HA!"
    card = Card.create_from_path("card", "Omri", "/home/user/Pictures/panda.jpg", "what?", solution)
    card.image.encrypt(card.solution)
    data = card.serialize()
    card2 = Card.deserialize(data)
    if True:
        card2.solution = solution
    print()
    print("origin:")
    print()
    print(card)
    print()
    print("fake:")
    print()
    print(card2)
    assert (repr(card) == repr(card2))
    card2.image.image.show()  # will show the same image as in path
