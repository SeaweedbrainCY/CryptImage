from cryptimage.cryptImage import CryptImage
from hashlib import sha256
from ecdsa import SigningKey, VerifyingKey
from binascii import b2a_base64
import base64
"""
    Perform all cryptography on images and data
"""

class Cryptography(CryptImage):
    unique_key = ""
    sys_public_key = VerifyingKey.from_pem(b'-----BEGIN PUBLIC KEY-----\nMHYwEAYHKoZIzj0CAQYFK4EEACIDYgAE7Nwsv9YBllR9m2N4vMXSBr5iZYJ5NmAX\nXJqzCkvBE0d6lFZyjzflz4IHLGHldAABF4VhJMMdcmaufBe9YYW0jhqsX5p2rN0V\nCTQeXuWsYshNOcmJF27/Iesj4IdMvPBW\n-----END PUBLIC KEY-----\n')
    sys_private_key = SigningKey.from_pem(b'-----BEGIN EC PRIVATE KEY-----\nMIGkAgEBBDDCgoVIMg+EEh7Qc3LaNJKJqLrb0PTJt68oCZ047Z5xpceuJbN8G170\nRiaiW0XorUOgBwYFK4EEACKhZANiAATs3Cy/1gGWVH2bY3i8xdIGvmJlgnk2YBdc\nmrMKS8ETR3qUVnKPN+XPggcsYeV0AAEXhWEkwx1yZq58F71hhbSOGqxfmnas3RUJ\nNB5e5axiyE05yYkXbv8h6yPgh0y88FY=\n-----END EC PRIVATE KEY-----\n')

    hashed_password = ""


    def __init__(self, imageURL, password):
        super().__init__(imageURL, password)
        self.hash_user_password()
        

    """
        Private
        Hash the user password
    """
    def hash_user_password(self):
        self.hash_user_password = sha256(self.password.encode())


    """
        Public
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
        Return the signed message in base64
    """
    def sign(self, clear):
        hexa =  self.sys_private_key.sign(clear.encode())  # Give the signed message in hexadecimal
        return self.hex_to_base64(hexa)

   

    """
        Verify the digital signature with the sys public key
        The signature must be a base64 string and the message a string.
        Return true if the signature is valide, false if not
    """
    def verify_signature(self, signature, message):
        encodedMessage = message.encode()
        signatureData = self.base64_to_hex(signature)
        try :
            self.sys_public_key.verify(signatureData,encodedMessage)
        except:
            return False
        return True
        

    


    """
        Convert hex bytes to base64 string
    """
    def hex_to_base64(self,encoded):
        return b2a_base64(encoded).decode()

    """
        Convert base64 string to hex bytes
    """
    def base64_to_hex(self, encoded):
        return base64.b64decode(encoded)



    





    