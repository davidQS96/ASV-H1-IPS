from skimage import io
from skimage import color
from skimage.transform import rescale
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import numpy
import math


"""
importar requiere el nombre del archivo como string

la función retorna la imagen en color o escala de grises según los requirimientos
una variable booleana que es verdadera si la imagen esta en RGB
una tuple con las dimenciones de la imagen

"""
def importar(direccion):
    img = io.imread(direccion)
    dimen = img.shape
    tamaño = len(dimen)
    dimen = dimen[0:2]
    if tamaño < 3:
        color = False
    else:
        color = True
    if color == True:
        red = img[:,:,0]
        green = img[:,:,1]
        igual = red == green
        grey = igual.all()
        if grey == True:
            img = red
    return img, color, dimen
