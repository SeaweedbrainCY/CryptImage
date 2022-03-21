from cryptimage.imageToVerify import ImageToVerify
from cryptimage.imageToSign import ImageToSign

"""
    Perform all cryptography on images and data
"""

class Cryptography(ImageToVerify, ImageToSign):
    unique_key = ""
    sys_public_key = ""
    hashed_password = ""


    def __init__(self):
        self.hash_user_password()
        self.generate_unique_key()
        

    """
        Hash the user password
    """
    def hash_user_password(self):
        pass


    """
        Generate the unique key (per user) according to the crypto schema 
    """
    def generate_unique_key(self):
        pass

    """
        Encrypt with the unique key
    """
    def encrypt(self, clear):
        pass

    """
        Decrypt with the unique key
    """
    def decrypt(self, cipher):
        pass

    """
        Sign with the sys private key
    """
    def sign(self, clear):
        pass

    """
        Verify the digital signature with the sys public key
    """
    def verify_signature(self, signed):
        pass

    






    