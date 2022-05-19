from cryptimage.cryptography import Cryptography
from cryptimage.lsb import LSB

class ImageToVerify(Cryptography, LSB):
    imageURL: str # Current path of the image to verify
    password: str # Password given by the user

    def __init__(self, imageURL, password):
        super().__init__(imageURL, password)
        self.imageURL = imageURL
        self.password = password
        self.main()


    def main(self):
        self.mainLSBVerify()
        if self.mainWatermarkVerify() :
            print("[*]\n[*] Verification de propriété valide")
            return True
        else:
            print("[*]\n[*] Verification de propriété invalide. UTILISATION DE L'IMAGE INTERDITE")
            return False
