"""
        Generate the watermark and embed it in the image which path is super.imageURL
"""
from cryptimage.cryptImage import CryptImage
from scipy import misc
import qrcode
import numpy as np
import imageio
from PIL import Image,ImageDraw
from random import randint

class Watermark(CryptImage) : 
    watermark_str = "" # The string to embed in the image
    finalImageURL = "" # Final path of the image signed

    qrcodePath = "qrcode_genere.png" # PRIVATE. Path to the tmp qr code


    def __init__(self, watermark_str):
        if watermark_str == "" or watermark_str == None:
            raise Exception("FATAL ERROR : No watermark to embed")
        self.watermark_str = watermark_str
        self.main()
    
    """
        Manage the watermark creation 
        Return True or  raise an exception if fail
    """
    def main(self):
        newPath = self.imageCopy() 
        watermarkPosition = self.generateRandomPosition()
        self.generateWatermarkImage()
        self.emebedWatermark(watermarkPosition)
        if newPath == None or watermarkPosition == None :
            raise Exception("FATAL ERROR : the signed-image to be or the watermark position are unknown")
        super.signedImagePath = newPath
        super.watermarkPosition = watermarkPosition 
        return True


    """
        Generate the image related to the watermark
    """
    def generateWatermarkImage(self):
        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=0)
        qr.add_data(self.watermark_str)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black",back_color="white").convert('RGB')
        img.save(self.qrcodePath)

    """
    Enlever les 3 carrés délimitant le QRcode
    """    
    def StripQRCodeCorners(self):   
        qr = Image.open(self.qrcodePath)
        qr_code = np.array(qr) 
        transparent_area = (0,0,79,79) #carré en haut à gauche
        transparent_area2=(qr_code.shape[0]-80,0,qr_code.shape[0],79) #carré en haut à droite
        transparent_area3=(0,qr_code.shape[0]-80,79,qr_code.shape[0]) #carré en bas à gauche
        mask=Image.new('L', qr.size, color=255)
        draw=ImageDraw.Draw(mask) 
        draw.rectangle(transparent_area, fill=0)
        draw2=ImageDraw.Draw(mask)
        draw2.rectangle(transparent_area2, fill=0)
        draw3=ImageDraw.Draw(mask)
        draw3.rectangle(transparent_area3,fill=0)
        qr.putalpha(mask)
        qr.save(self.qrcodePath)


    """
        Copy and create the signed-image to be in the right location
    """
    def imageCopy(self):
        pass


    """
        Verify if the image is encoded in PNG. If not, make the convertion
        If any conversion is made, the copied image is deleted and replaced by the converted one
    """

    def convertToPNG(self):
        pass

    """
        Generate a random position in the image where the watermark CAN be embedded
    """
    def generateRandomPosition(self):
        M = misc.imread(self.imageURL)
        M.shape
        i_qr = random.randint(qr.shape,M.shape-qr.shape-1) #abscisse du QR code
        j_qr = random.randint(qr.shape,M.shape-qr.shape-1) #ordonnée du QR code


    """
        Embed the generated watermark (as an image) in the image
    """
    def emebedWatermark(self, position):
        if position == None:
            raise Exception("FATAL ERROR : No position to embed watermark")
        pass


