from cryptimage.cryptImage import CryptImage
from hashlib import sha256
from ecdsa import SigningKey, VerifyingKey
from binascii import b2a_base64
import base64
import ecies
import os
import mysql.connector
from difflib import SequenceMatcher

"""
    Perform all cryptography on images and data
"""

class Cryptography():
    imageURL = ""
    password = ""
    unique_key = ""
    # Curve : SECP256k1
    sys_public_key = VerifyingKey.from_pem(b'-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE4BCAAs7qnPl6aQK9FrzyDOf63glR2JSS\nQqi6vuVLepKfq9Kzi5R3DlAiVMg0gUrQT2QUVHpuEi0Smb+j2xZoRA==\n-----END PUBLIC KEY-----\n')
    sys_private_key = SigningKey.from_pem(b'-----BEGIN EC PRIVATE KEY-----\nMHQCAQEEIOwpju4BFTHMclLsT2Gm549ZRB4IsZUDrTFy9BjAzneOoAcGBSuBBAAK\noUQDQgAE4BCAAs7qnPl6aQK9FrzyDOf63glR2JSSQqi6vuVLepKfq9Kzi5R3DlAi\nVMg0gUrQT2QUVHpuEi0Smb+j2xZoRA==\n-----END EC PRIVATE KEY-----\n')

    hashed_password = ""



    def __init__(self, imageURL, password):
        self.imageURL = imageURL
        self.password = password
        self.hash_user_password()


    """
        Private
        Hash the user password
    """
    def hash_user_password(self):
        self.hashed_password = sha256(self.password.encode()).hexdigest()


    """
        Public
        Generate the unique key (per user) according to the crypto schema
    """
    def generate_unique_key(self):
        encrypted_password = self.encrypt(self.hash_user_password)
        self.unique_key = sha256(encrypted_password.encode()).hexdigest()


    """
        Encrypt with the public key
        Clear must be a utf8 string
    """
    def sys_encrypt(self, clear):
        public_key_hex = "0x" + self.sys_public_key.to_string().hex()
        clear_data = clear.encode()
        encrypted = ecies.encrypt(public_key_hex, clear_data)
        return (encrypted.hex())


    """
        Decrypt with the private key
        cipher must be a an hex encoded string
    """
    def sys_decrypt(self, cipher):
        private_key_hex = "0x" + self.sys_private_key.to_string().hex()
        print("priv= " , private_key_hex)
        cipher_data = bytes.fromhex(cipher)
        decrypted = ecies.decrypt(private_key_hex, cipher_data)
        return self.readablize(decrypted)



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


    def readablize(self, b: bytes) -> str:
        try:
            return b.decode()
        except ValueError:
            return b.hex()



    """
        Calculate the Neural hash of the image
    """
    def hash_image(self) -> str :
        try :
            image_hash_str = os.popen("cd /home/admin/; python3 AppleNeuralHash2ONNX/nnhash.py AppleNeuralHash2ONNX/NeuralHash/model.onnx AppleNeuralHash2ONNX/NeuralHash/neuralhash_128x96_seed1.dat " + self.imageURL).read()
        except :
            raise Exception("Impossible to calculate the image hash")

        return image_hash_str.strip()



    """
        Stock the hash in the bdd after the signature
    """
    def stock_image_neural_hash(self) :
        neural_hash = self.hash_image()
        passwordFile = open("/home/admin/CryptImage/cryptimage/bdd_passwd.txt", mode='r')
        passwd = str(passwordFile.readline()).strip()
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password=passwd,
        database="CryptImage"
        )
        neural_hash = neural_hash.strip()
        mycursor = mydb.cursor()
        sql = "INSERT INTO hashs (hash) VALUES ('" + neural_hash + "');"
        mycursor.execute(sql)
        mydb.commit()


    """
        retrieve hash in the bdd and calculate the correlation rate
    """


    def checkHashStorage(self)  :
         neural_hash = self.hash_image()
         passwordFile = open("/home/admin/CryptImage/cryptimage/bdd_passwd.txt", mode='r')
         passwd = str(passwordFile.readline()).strip()
         mydb = mysql.connector.connect(
         host="localhost",
         user="root",
         password=passwd,
         database="CryptImage"
         )
         neural_hash = neural_hash.strip()
         mycursor = mydb.cursor()
         sql = "SELECT * from hashs"
         mycursor.execute(sql)
         hashs = mycursor.fetchall()
         for h in hashs :
             _,h = h
             if self.similar(h, neural_hash) >=0.7:
                 return True
         return False


    def similar(self,a, b):
        return SequenceMatcher(None, a, b).ratio()

