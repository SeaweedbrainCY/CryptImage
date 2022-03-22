"""
        Generate the watermark and embed it in the image which path is super.imageURL
"""
from hashlib import sha256
from os import lseek
from cryptimage.cryptImage import CryptImage
from cryptimage.cryptography import Cryptography
from cryptimage.neuralHash import NeuralHash
from scipy import misc
import qrcode
import numpy as np
import imageio
from PIL import Image,ImageDraw
from random import randint

class Watermark(CryptImage) : 
    watermark_str = "" # The string to embed in the image
    finalImageURL = "" # Final path of the image signed
    watermarkPosition = "" # un dictionnaire de la forme : {'top_left' : (x,y), 'top_right' : (x,y)}

    qrcodePath = "qrcode_genere.png" # PRIVATE. Path to the tmp qr code
    qrCodePixelsBytes = [] # Matrice stockant les pixels du QR code 1: blanc, 0: noir

    def __init__(self, imageURL, password):
        super().__init__(imageURL, password)
        self.generateWatermarkString()
    
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
        self.finalImageURL = newPath
        self.watermarkPosition = watermarkPosition 
        return True


    """
        Generate the string to embed in the watermark
    """
    def generateWatermarkString(self):
        neuralHash = NeuralHash()
        crypto = Cryptography(self.imageURL, self.password)

        imageHash = '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08'#neuralHash.neuralHash() for test purpose
        hash_password_binary = ''.join(format(ord(x), 'b').zfill(8) for x in crypto.hashed_password) # Encoding over 8 bits per char
        neuralHash_binary = ''.join(format(ord(x), 'b').zfill(8) for x in imageHash) # Encoding over 8 bits per char
        text_to_hash_binary = bin(int(hash_password_binary,2) | int(neuralHash_binary,2))[2:]
        text_to_hash_hexa = hex(int(text_to_hash_binary, 2))
        hashed_text = sha256(text_to_hash_hexa[2:].encode()).hexdigest()
        hashed_text_signed = crypto.sign(hashed_text)
        self.watermark_str = hashed_text + "," + hashed_text_signed




    """
        Generate the image related to the watermark
    """
    def generateWatermarkImage(self):
        qr = qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_H,box_size=10,border=0)
        qr.add_data(self.watermark_str)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black",back_color="white").convert('RGB')
        img.save(self.qrcodePath)
        self.stripQRCodeCorners()

    """
    Enlever les 3 carrés délimitant le QRcode
    """    
    def stripQRCodeCorners(self):   
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
    def emebedWatermark(self):

        self.watermarkPosition = {"top_left" : (0,0), "bottom_left" : (1,1)}
        self.finalImageURL = "/Users/stchepinskynathan/Downloads/test.png"
        self.qrCodePixelsBytes = [[0,0], [1,1]]
        (top_left_x, top_left_y) = self.watermarkPosition["top_left"]
        (top_right_x, top_right_y) = self.watermarkPosition["bottom_left"]

       
        im = Image.open(self.finalImageURL)
        pixelMap = im.load()
        x=0
        y=0
        for i in range(top_left_x, top_right_x+1):
            for j in range(top_left_y, top_right_y+3, 3):
                pixel = pixelMap[i,j]
                (r,g,b, a) = pixel
                (new_r, new_g, new_b) = (r,g,b)
                if j < top_right_y + 1:
                    new_r = int(str(bin(r)[2:-1]) + str(self.qrCodePixelsBytes[x][y]), 2)
                if j+1 < top_right_y + 1:
                    new_g = int(bin(g)[2:-1] + str(self.qrCodePixelsBytes[x][y+1]), 2)
                if j+2 < top_right_y + 1:
                    new_b = int(bin(b)[2:-1] + str(self.qrCodePixelsBytes[x][y+2]),2)
                pixelMap[i,j] = (new_r, new_g, new_b,a)
                y+=1
            x+=1
            y=0
        im.save(self.finalImageURL)





    """
        Extract the generated watermark (as an image) from the image
    """
    def extractWatermark(self):
        self.watermarkPosition = {"top_left" : (0,0), "bottom_left" : (1,1)}
        self.imageURL = "/Users/stchepinskynathan/Downloads/test.png"
        (top_left_x, top_left_y) = self.watermarkPosition["top_left"]
        (top_right_x, top_right_y) = self.watermarkPosition["bottom_left"]


        im = Image.open(self.imageURL)
        pixelMap = im.load()
        x=0
        y=0
        qrCodeExtracted = []
        for i in range(top_left_x, top_right_x+1):
            tmp = [] 
            for j in range(top_left_y, top_right_y+3, 3):
                pixel = pixelMap[i,j]
                (r,g,b, a) = pixel
                if j < top_right_y + 1:
                    tmp.append(str(bin(r)[-1]))
                if j+1 < top_right_y + 1:
                    tmp.append(str(bin(g)[-1]))
                if j+2 < top_right_y + 1:
                    tmp.append(str(bin(b)[-1]))
                y+=1
            qrCodeExtracted.append(tmp)
            x+=1
            y=0
        self.qrCodePixelsBytes = qrCodeExtracted
        print(qrCodeExtracted)
        


        


