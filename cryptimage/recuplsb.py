##Récupérer les lsb d'une image png
# import numpy as np
#
# from PIL import Image
# from numpy import asarray
# img = Image.open(r"C:\cryptimage\blue.png")
# pix = np.array(asarray(img))
# pixb = []
# lsb = []
# for i in range(len(pix)):
#     for j in range(len(pix[i])):
#         for k in range(len(pix[i][j])):
#             pixb.append(bin((pix[i][j][k])))
# for i in range (len(pixb)):
#     lsb.append(pixb[i][-1:])

##decodage

# import qrcode
#
# qr = qrcode.QRCode(
#     version=1,
#     error_correction=qrcode.constants.ERROR_CORRECT_H,
#     box_size=10,
#     border=1,)
#
# qr.add_data('101010') #on met la matrice de bits ici
# qr.make(fit=True)
# img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
# img.show()

##Lecture d'un qrcode

import cv2

import cv2
img = cv2.imread("C:\cryptimage\qtest1.PNG") #L'image à lire
detector = cv2.QRCodeDetector()

data, bbox, straight_qrcode = detector.detectAndDecode(img)

if bbox is not None:
    print(f"QRCode data:\n{data}")
    n_lines = len(bbox)
    for i in range(n_lines):
        point1 = tuple(bbox[i][0])
        point2 = tuple(bbox[(i+1) % n_lines][0])
        cv2.line(img, point1, point2, color=(255, 0, 0), thickness=2)


