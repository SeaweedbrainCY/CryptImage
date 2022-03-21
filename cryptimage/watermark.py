"""
        Generate the watermark and embed it in the image which path is super.imageURL
"""
from cryptimage.cryptImage import CryptImage


class Watermark(CryptImage) : 
    watermark_str: str # The string to embed in the image

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
        pass 

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
        pass

    """
        Embed the generated watermark (as an image) in the image
    """
    def emebedWatermark(self, position):
        if position == None:
            raise Exception("FATAL ERROR : No position to embed watermark")
        pass


