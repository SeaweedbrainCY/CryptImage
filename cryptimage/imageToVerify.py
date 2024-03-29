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
        try :
            self.mainLSBVerify()
            lsb = True
        except :
            lsb = False
        try :
            watermark = self.mainWatermarkVerify()
        except :
            watermark = False



        if lsb == watermark:
            print("[*]\n[*] SUCCESS : Verification de propriété valide")
            return True
        else:
            print("[*]\n[*]FORBIDDEN :  Verification de propriété invalide. UTILISATION DE L'IMAGE INTERDITE")
            return False
