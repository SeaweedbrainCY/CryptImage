from cryptimage.cryptImage import CryptImage

class ImageToSign(CryptImage):
    imageURL: str # Current path of the image to verify
    password: str # Password given by the user
    signedImagePath : str # current path of the signed image or signed-image to be
    watermark_position : str # the position of the watermark in the image

    def __init__(self):
        self.imageURL = super.imageURL
        self.password = super.password

