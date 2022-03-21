from cryptimage.cryptImage import CryptImage

"""
    Perform all cryptography on images and data
"""

class Cryptography(CryptImage):
    unique_key = ""
    sys_public_key = ""
    hashed_password = ""


    def __init__(self, imageURL, password):
        super().__init__(imageURL, password)
        

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

    


    





    