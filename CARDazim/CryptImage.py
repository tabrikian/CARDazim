from PIL import Image
import hashlib
from Crypto.Cipher import AES


class CryptImage:
    def __init__(self, image: Image, key_hash: bytes = None) -> None:
        self.image = image
        self.key_hash = key_hash
        self.length = 0
        self.height = 0
        if self.image is not None:
            start_x, start_y, end_x, end_y = self.image.getbbox()
            self.length = end_x - start_x
            self.height = end_y - start_y

    @staticmethod
    def create_from_path(path: str) -> "CryptImage":
        img = Image.open(path, mode="r")
        return CryptImage(img)

    @staticmethod
    def bytes_to_image(image_data: bytes, length: int, height: int) -> "CryptImage":
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

        hash_key = image_data[-32:]
        return CryptImage(image, hash_key)

    def image_to_bytes(self) -> bytes:
        img = self.image.load()
        image_data = int(1).to_bytes(1, "big")
        for i in range(self.height):
            for j in range(self.length):
                pix = img[j, i]
                for c in range(3):
                    image_data += pix[c].to_bytes(1, "big")
        return image_data[1:]

    def encrypt(self, key: str) -> None:
        hash_object = hashlib.sha256(key.encode())
        hashed_key = hash_object.digest()
        plaintext = self.image_to_bytes()
        cipher = AES.new(hashed_key, AES.MODE_EAX, nonce=b'arazim')
        encrypted = cipher.encrypt(plaintext)
        self.image = self.bytes_to_image(encrypted, self.length, self.height).image
        hash_object = hashlib.sha256(hashed_key)
        self.key_hash = hash_object.digest()

    def decrypt(self, key: str) -> bool:
        hash_object = hashlib.sha256(key.encode())
        hashed_key = hash_object.digest()

        hash_object = hashlib.sha256(hashed_key)
        hashed_key = hash_object.digest()

        if hashed_key != self.key_hash:
            return False

        self.key_hash = None
        hash_object = hashlib.sha256(key.encode())
        hashed_key = hash_object.digest()
        encrypted = self.image_to_bytes()
        cipher = AES.new(hashed_key, AES.MODE_EAX, nonce=b'arazim')
        decrypted = cipher.decrypt(encrypted)
        self.image = self.bytes_to_image(decrypted, self.length, self.height).image
        return True
