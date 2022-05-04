from cryptimage.cryptography import Cryptography
from cryptimage.lsb import LSB
from cryptimage.watermark import Watermark


class ImageToSign(Cryptography, LSB):
    imageURL= "" # Current path of the image to verify
    password= "" # Password given by the user
    signedImagePath : str # current path of the signed image or signed-image to be
    watermark_position : str # the position of the watermark in the image

    def __init__(self, imageURL, password):
        super().__init__(imageURL, password)
        self.imageURL = imageURL
        self.password = password
        self.main()

    def main(self):
        if self.mainWatermarkSignature() :
            if  self.mainLSBSignature() :
                name = self.imageURL.split('.')
                print("[*] Votre image a été protégée avec succès ! L'image signée est : " , name[0] , "_signed." , name[1])
            
        else :
            raise Exception("FATAL ERROR : An error occured with generating the watermark")
        



