from skimage import io
from skimage import color
from skimage.transform import rescale
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import numpy
import math
from skimage.filters.rank import median
from skimage.morphology import disk

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
            color = False
    return img, color, dimen


"""
filtrosalpimienta 
entradas
imagen: imagen que se desea modificar color o grises
color: valor booleano, true si es a color o false si es grises
intensidad: valor booleano, true para elevado o false para moderado
crojo,cverde,cazul: valor booleano, opcional, true si se desea modificar un canal

la función retorna la imagen filtrado

"""
def filtrosalpimienta(imagen,color,intensidad,crojo=None,cverde=None,cazul=None):
    if intensidad == True:
        dureza = 3
    else:
        dureza = 1
    if color == True:
        red = imagen[:,:,0]
        green = imagen[:,:,1]
        blue = imagen[:,:,2]
        final = imagen
        if crojo == True:
            finalr = median(red,disk(dureza)) 
            final[:,:,0] = finalr
        if cverde == True:
            finalg = median(green,disk(dureza)) 
            final[:,:,1] = finalg
        if cazul == True:
            finalb = median(blue,disk(dureza))  
            final[:,:,2] = finalb
    else:
        final = median(imagen,disk(dureza))
    return final