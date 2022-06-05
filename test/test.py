from cryptimage.cryptography import Cryptography
from cryptimage.lsb import LSB
from cryptimage.watermark import Watermark
import random

import string


import os, sys

class HiddenPrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout

def lsb_test():
   with HiddenPrints() :
        furl  = "/home/admin/CryptImage/test/image/image_signed.png"
        lsb = LSB(furl, "passwordForTest")
        lsb.finalImageURL = furl
        initial = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(100))
        lsb.lsb_str = initial
        lsb.embedInLSB()
        lsb.decodeLSB()
   assert initial in lsb.lsb_str, "LSB encoded isn't the same than decoded"

def watermark_string_generation_test():
    with HiddenPrints() :
        url = "/home/admin/CryptImage/test/image/image.png"
        furl  = "/home/admin/CryptImage/test/image/image_signed.png"
        watermark = Watermark(url, "passwordForTest")
        watermark.generateWatermarkString()
        result = watermark.checkWatermark()
    assert result, "watermark string check should be true"

    with HiddenPrints() :
        watermark.watermark_str = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(100))
        result = watermark.checkWatermark()
    assert not result, "watermark string check should be false"


def watermark_qrcode_generation_test():
    with HiddenPrints():
         url = "/home/admin/CryptImage/test/image/image.png"
         furl  = "/home/admin/CryptImage/test/image/image_signed.png"
         w = Watermark(url, "passwordForTest")
         w.finalImageURL = furl
         w.generateWatermarkString()
         w.generateWatermarkImage()
         w.stripQRCodeCorners()
         w.generateQrCodeMatrice()
         w.reconstructQRCode()
         w.refaire_3_blocs()
         w.addBorder()
         w.readQRcode()
         isOk = w.checkWatermark()

         assert isOk, "The watermark generation should be decoded"

         w = Watermark(url, "passwordForTest")
         w.finalImageURL = furl
         w.generateWatermarkString()
         w.generateWatermarkImage()
         w.password  = "fakePasswordForTest"
         w.stripQRCodeCorners()
         w.generateQrCodeMatrice()
         w.reconstructQRCode()
         w.refaire_3_blocs()
         w.addBorder()
         w.readQRcode()
         isOk = w.checkWatermark()
         assert not isOk, "The watermark generation should fail"


def hash_storage_test():
    with HiddenPrints():
        url = "/home/admin/CryptImage/test/image/image.png"
        c = Cryptography(url, "passwordForTest")
        image_h = c.hash_image()
        c.stock_image_neural_hash()
        isStored = c.checkHashStorage()

        assert isStored, "The hash should be stored"



if __name__ == "__main__":
    lsb_test()
    watermark_string_generation_test()
    watermark_qrcode_generation_test()
    hash_storage_test()
    print("All test passed")
