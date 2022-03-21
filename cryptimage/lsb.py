"""
        Generate the string related to the watermark position to embed in the LSB of image
"""
from cryptimage.cryptImage import CryptImage

class LSB(CryptImage):
    lsb_str = "" # the string to embed in LSB 

    def __init__(self):
        self.main()


    
    """
        Manage the LSB creation and embedding
        Return True or  raise an exception if fail
    """
    def main(self):
        self.generateLSBstring()
        self.embedInLSB()

    


    """
        Generate the LSB string 
    """
    def generateLSBstring(self):
        pass

    """
       Embed the LSB string in the PNG
    """
    def embedInLSB(self):
        if self.lsb_str == "":
            raise Exception("FATAL ERROR : There is no string to embed in LSB")
        pass
