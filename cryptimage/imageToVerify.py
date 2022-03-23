from cryptimage.cryptography import Cryptography
from cryptimage.watermark import Watermark

class ImageToVerify(Cryptography, Watermark):
    imageURL: str # Current path of the image to verify
    password: str # Password given by the user

    def __init__(self, imageURL, password):
        super().__init__(imageURL, password)
        self.imageURL = imageURL
        self.password = password

