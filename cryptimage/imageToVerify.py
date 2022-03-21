from cryptimage.cryptImage import CryptImage

class ImageToVerify(CryptImage):
    imageURL: str # Current path of the image to verify
    password: str # Password given by the user

    def __init__(self):
        self.imageURL = super.imageURL
        self.password = super.password

