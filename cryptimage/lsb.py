"""
        Generate the string related to the watermark position to embed in the LSB of image
"""
from cryptimage.aes import AESCipher
from cryptimage.cryptography import Cryptography
from cryptimage.watermark import Watermark
from PIL import Image
import base64
import json
class LSB(Watermark):
    lsb_str = "" # The string to embed in LSB

    def __init__(self, imageURL, password):
        super().__init__(imageURL, password)
    """
        Manage the LSB creation and embedding
        Return True or  raise an exception if fail
    """
    def main(self):
        self.generateLSBstring()
        self.embedInLSB()

    """
        Genere le message chiffre a integrer dans les LSB
    """
    def generateLSBstring(self):
        position = self.watermarkPosition
        print(position)
        position_str = json.dumps(position)
        crypto = Cryptography(self.imageURL, self.password)
        aes = AESCipher(crypto.unique_key)
        encrypted = aes.encrypt(position_str).decode()
        
        signed = crypto.sign(encrypted)
        self.lsb_str = encrypted + "&" + signed + "&"
        

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
            watermarkPosition  = json.load(decrypted)
        except:
            raise Exception("**CRITIC** FATAL ERROR : Embedded information are corrupted but verified")

        self.watermarkPosition  = watermarkPosition

        


    """
       Code le message dans la premiere colonne de pixel de l'image
    """
    def embedInLSB(self):
        #Importation de l'image a encoder
        im = Image.open("original.png")
        width, height = im.size
        pixels = im.load()

        if self.lsb_str == "":
            raise Exception("FATAL ERROR : There is no string to embed in LSB") 

        #Conversion en binaire du Str à encoder
        bin_lsb_str = ''.join(format(ord(x), 'b').zfill(8) for x in self.lsb_str)        
        i = 0

        #On parcourt la premiere ligne de pixel de longueur notre message
        print(len(bin_lsb_str))
        for x in range(0, len(bin_lsb_str), 3):  
            #print(x)            
            r,g,b,_=pixels[x,0]                        
            if i<len(bin_lsb_str):
                r_bit, g_bit, b_bit = bin(r), bin(g), bin(b)

                #On extrait les LSB de chaque code rgb
                #r_lsb, g_lsb, b_lsb = int(r_bit[-1]), int(g_bit[-1]), int(b_bit[-1])           

                #On modifie chaque R G B avec le code voulu
                new_r_lsb, new_g_lsb, new_b_lsb = bin_lsb_str[i], bin_lsb_str[i+1], bin_lsb_str[i+2]       
                
                #On reconstitue nos octets pour chaque R G B
                final_embed_r_bit = int(r_bit[:-1] + str(new_r_lsb), 2)
                final_embed_g_bit = int(g_bit[:-1] + str(new_g_lsb), 2)
                final_embed_b_bit = int(b_bit[:-1] + str(new_b_lsb), 2)


        #On code nos octets dans l'image
        pixels[x,0] = (final_embed_r_bit, final_embed_g_bit, final_embed_b_bit)
        print(pixels[x,0])
        
        im.save("original.png")
        #Penser a passer a la ligne si on depasse la longueur de l'image par rapport a la longueur du 

    """
        Decode le message contenu dans les LSB de la premiere colonne de pixel de l'image
    """
    def decodeLSB(self):
        im = Image.open("original.png") #TEST1 iwQnPxC+du2YxYmkdmDOFuIUgt2fOu/Mwn+YxaViYZo=

        chars = ""
        extracted = ""
        pixels = im.load()

        c = 0       #Compteur du caractere d'arret

        for x in range(0,im.width): 
            r,g,b,_= pixels[x,0]

            #On extrait les LSB de chaque pixel (R G B)
            extracted += bin(r)[-1]
            extracted += bin(g)[-1]
            extracted += bin(b)[-1]

            if(len(extracted)==8):

                #Décodage binaire
                chars.append(chr(int(''.join([str(bit) for bit in extracted]), 2)))

                #Verification de caractère d'arret
                if chars[-1] == "&":
                    if c == 0:
                        c +=1
                    else:
                        pass
        
        
        self.lsb_str = chars
        print(self.lsb_str)




