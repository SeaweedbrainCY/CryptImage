##Récupérer les lsb d'une image png
import numpy as np

from PIL import Image
from numpy import asarray
img = Image.open(r"C:\cryptimage\blue.png")
pix = np.array(asarray(img))
pixb = []
lsb = []
for i in range(len(pix)):
    for j in range(len(pix[i])):
        for k in range(len(pix[i][j])):
            pixb.append(bin((pix[i][j][k])))
for i in range (len(pixb)):
    lsb.append(pixb[i][-1:])

##








