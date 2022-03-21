"""
        Generate the string related to the watermark position to embed in the LSB of image
"""
from cryptimage.cryptImage import CryptImage
import bitarray
import base64

class LSB(CryptImage):
    lsb_str = "" # The string to embed in LSB


    
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
        encoded_message = base64.b64encode(self.lsb_str)
        
        #Convertion du message en bit
        ba = bitarray.bitarray()
        ba.frombytes(encoded_message.encode('utf-8'))
        bit_array = [int(i) for i in ba]

    """
       Embed the LSB string in the PNG
    """
    def embedInLSB(self, txt):
        if self.lsb_str == "":
            raise Exception("FATAL ERROR : There is no string to embed in LSB") 

        i = 0
        for x in range(0, len(self.bitarray), 3):              #On parcourt la première ligne de pixel de longueur notre message
            r,g,b = self.pixels[x,0]                        

            if i<len(self.bit_array):
                r_bit, g_bit, b_bit = bin(r), bin(g), bin(b)
                r_lsb, g_lsb, b_lsb = int(r_bit[-1]), int(g_bit[-1]), int(b_bit[-1])           #On extrait les LSB de chaque code rgb
                new_r_lsb, new_g_lsb, new_b_lsb = self.bit_array[i], self.bit_array[i+1], self.bit_array[i+2]       #On modifie chaque R G B avec le code voulu
                
                #On reconstitue nos octets pour chaque r g b
                final_embed_r_bit = int(r_bit[:-1] + str(new_r_lsb), 2)
                final_embed_g_bit = int(g_bit[:-1] + str(new_g_lsb), 2)
                final_embed_b_bit = int(b_bit[:-1] + str(new_b_lsb), 2)

        #On code nos octets dans l'image
        self.pixels[x,0] = (final_embed_r_bit, final_embed_g_bit, final_embed_b_bit)

#Penser à passer à la ligne si on depasse la longueur de l'image par rapport à la longueur du message