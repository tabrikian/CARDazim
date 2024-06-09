from PIL import Image


class CryptImage:
    def __init__(self, image: Image, key_hash: bytes = None):
        self.image = image
        self.key_hash = key_hash
        self.length = 0
        self.height = 0
        if self.image is not None:
            start_x, start_y, end_x, end_y = self.image.getbbox()
            self.length = end_x - start_x
            self.height = end_y - start_y
            print(self.length, self.height)

    @staticmethod
    def create_from_path(path: str):
        img = Image.open(path, mode="r")
        return CryptImage(img)

    def encrypt(self, key: str) -> None:
        pass

    def decrypt(self, key: str) -> bool:
        pass
