"""
        Generate the string related to the watermark position to embed in the LSB of image
"""
from cryptimage.aes import AESCipher
from cryptimage.cryptography import Cryptography
from cryptimage.watermark import Watermark
from PIL import Image
import base64
import json
import sys
from hashlib import *
class LSB(Watermark):
    lsb_str = "" # The string to embed in LSB

    def __init__(self, imageURL, password):
        super().__init__(imageURL, password)
    """
        Manage the LSB creation and embedding
        Return True or  raise an exception if fail
    """
    def mainLSBSignature(self):
        print("[*] Génération des données cachées ...", end=' ')
        self.generateLSBstring()
        print("Ok")

        print("[*] Intégration des données cachées dans l'image ...", end=' ')
        self.embedInLSB()


        print("[*] Stockage du haché neuronnal dans la base de donnée ...", end=' ')
        crypto = Cryptography(self.imageURL, self.password)
        crypto.stock_image_neural_hash()
        print("Ok")
        return True

    def mainLSBVerify(self):
        print("[*] Extraction des données cachées dans l'image ...",  end=' ')
        self.decodeLSB()
        print("Ok")

        print("[*] Déchiffrement des données cachées ...",  end=' ')
        self.decryptLSBString()
        print("Ok. Déchiffré : ", self.watermarkPosition )

    """
        Genere le message chiffre a integrer dans les LSB
    """
    def generateLSBstring(self):
        position = self.watermarkPosition
        position_str = json.dumps(position)
        crypto = Cryptography(self.imageURL, self.password)
        aes = AESCipher(crypto.unique_key)
        encrypted = aes.encrypt(position_str).decode()

        signed = crypto.sign(encrypted)
        self.lsb_str = encrypted + "&" + signed.strip() + "&"


    """
        decrypt the LSB string to retrieve the watermark position
        raise an error if the signature isn't valid
    """
    def decryptLSBString(self):
        crypto = Cryptography(self.imageURL, self.password)
        aes = AESCipher(crypto.unique_key)


        splited = self.lsb_str.split('&')
        if len(splited) != 3 :
            raise Exception("FATAL ERROR : Embedded information are corrupt")
        encrypted = splited[0]
        signed = splited[1]
        if not crypto.verify_signature(signed, encrypted):
            raise Exception("FATAL ERROR : Embedded information cannot be verified")
        try:
            decrypted = aes.decrypt(encrypted)
        except:
            raise Exception("**CRITIC** FATAL ERROR : Embedded information are corrupted but verified")
        try :
            watermarkPosition  = json.loads(decrypted)
        except :
            raise Exception("**CRITIC** FATAL ERROR : Embedded information are corrupted but decrypted")

        self.watermarkPosition  = watermarkPosition



    """
       Code le message dans la premiere colonne de pixel de l'image
    """
    def embedInLSB(self):
        #Importation de l'image a encoder
        im = Image.open(self.finalImageURL) # L'image a déjà été modifiée par watermark
        width, height = im.size
        pixels = im.load()

        if self.lsb_str == "":
            raise Exception("FATAL ERROR : There is no string to embed in LSB")

        #Conversion en binaire du Str à encoder
        bin_lsb_str = ''.join(format(ord(x), 'b').zfill(8) for x in self.lsb_str)
        i = 0
        x=0
        y = 0
        #On parcourt la premiere ligne de pixel de longueur notre message
        #print(len(bin_lsb_str))
        #print(self.lsb_str)
        for i in range(0, len(bin_lsb_str), 3):
            #print(x)
            if x> width: # on a atteint le bout de la ligne, on passe à la ligne suivante
                y += 1
                x=0
            if im.mode == "RGB":
                r,g,b=pixels[x,y]
            else :
                r,g,b,a =pixels[x,y]
            #print(x,y, " : ", r,g,b)

            r_bit, g_bit, b_bit = bin(r), bin(g), bin(b)

                #On extrait les LSB de chaque code rgb
                #r_lsb, g_lsb, b_lsb = int(r_bit[-1]), int(g_bit[-1]), int(b_bit[-1])

                #On modifie chaque R G B avec le code voulu
            final_embed_b_bit = b
            final_embed_g_bit = g
            final_embed_r_bit = r

                #On reconstitue nos octets pour chaque R G B
            if i < len(bin_lsb_str):
                final_embed_r_bit = int(r_bit[:-1] + str(bin_lsb_str[i]), 2)
            if i+1 < len(bin_lsb_str):
                final_embed_g_bit = int(g_bit[:-1] + str(bin_lsb_str[i+1]), 2)
            if i+2 < len(bin_lsb_str):
                final_embed_b_bit = int(b_bit[:-1] + str(bin_lsb_str[i+2]), 2)

            #print("initial = ", r_bit, g_bit, b_bit, end=' ')
            #if i+2 < len(bin_lsb_str):
                #print(bin( final_embed_r_bit ),bin(final_embed_g_bit) , bin(final_embed_b_bit) , end=' ')


            #On code nos octets dans l'image
            #print(bin_lsb_str[i],bin_lsb_str[i+1] ,bin_lsb_str[i+2], end='')
            if im.mode == "RGB" :
                pixels[x,y] = (final_embed_r_bit, final_embed_g_bit, final_embed_b_bit)
            else :
                pixels[x,y] = (final_embed_r_bit, final_embed_g_bit, final_embed_b_bit,a)

            x+=1
            #print(pixels[x,y], end=' ')
       #print(self.lsb_str)

        im.save(self.finalImageURL)
        #print(self.md5f("original.png"))
        #Penser a passer a la ligne si on depasse la longueur de l'image par rapport a la longueur du

    """
        Decode le message contenu dans les LSB de la premiere colonne de pixel de l'image
    """
    def decodeLSB(self):
        im = Image.open(self.imageURL) #TEST1 iwQnPxC+du2YxYmkdmDOFuIUgt2fOu/Mwn+YxaViYZo=
        width, height = im.size
        chars = ""
        extracted = ""
        pixels = im.load()

        spliter_counter = 0
        x,y = 0,0
        while spliter_counter != 2:
            if x >= width:
                y+= 1
                x=0
            if y >= height :
                raise Exception("FATAL ERROR : Impossible to retrieve hidden data. The file must be corrupted or not protected")
            if im.mode == "RGB":
                r,g,b = pixels[x,y]
            else :
                r,g,b,_ = pixels[x,y]
            #print(pixels[x,y], end=' ')
            r_bit = str(bin(r))[2:][-1]
            g_bit = str(bin(g))[2:][-1]
            b_bit = str(bin(b))[2:][-1]


            lsbits = [r_bit, g_bit, b_bit]

            for bit in lsbits:
                chars += bit

                if len(chars) == 8 : # On a un octet alors on convertit
                    #print(chars)
                    new_char = "".join([chr(int(chars[i:i+8], 2)) for i in range(0,len(chars),8)])
                    extracted += new_char
                    chars = ""
                    if new_char == "&":
                        spliter_counter += 1
                    #print(extracted)
            x+=1
        self.lsb_str = extracted






