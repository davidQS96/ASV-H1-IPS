from skimage import io
from skimage import color
from skimage.transform import rescale
import matplotlib.image as mpimg
from matplotlib import pyplot as plt
import numpy
import math
from skimage.filters.rank import median
from skimage.morphology import disk
from skimage.morphology import diamond
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
unsolocolor: valor booleano, true para filtrar en un solo color; necesita los valores roj,ver,azu
roj,ver,azu: valor de color en cada canal RGB

la función retorna la imagen filtrado

"""
def filtrosalpimienta(imagen,rgb,intensidad,unsolocolor,roj=None,ver=None,azu=None):
    if intensidad == True:
        dureza = 3
    else:
        dureza = 1
    if rgb == True:
        fil = imagen.copy()
        cont = 0
        while cont < 3:
            fil[:,:,cont] = median(imagen[:,:,cont],disk(dureza)) 
            cont = cont +1
        if unsolocolor == True:
          orig = imagen.copy()
          red = imagen[:,:,0] == roj
          green = imagen[:,:,1] == ver
          blue = imagen[:,:,2] == azu
          parte = red == green
          parte = parte == blue
          contraparte = ~parte 
          seccion = fil.copy()
          resto = orig.copy()
          a = 0
          while a < 3:
              seccion[:,:,a]=seccion[:,:,a]*parte
              resto[:,:,a]=resto[:,:,a]*contraparte
              a=a+1
          final = resto+seccion
        else:
            final = fil
    else:
        final = median(imagen,disk(dureza))
    return final


"""
filtrogaussiano
entradas
imagen: imagen que se desea modificar color o grises
color: valor booleano, true si es a color o false si es grises
intensidad: valor booleano, true para elevado o false para moderado
unsolocolor: valor booleano, true para filtrar en un solo color; necesita los valores roj,ver,azu
roj,ver,azu: valor de color en cada canal RGB

la función retorna la imagen filtrado

"""

def gaussiano(imagen,rgb,intensidad,unsolocolor,roj=None,ver=None,azu=None):
    if intensidad == True:
        dureza = 5
    else:
        dureza = 3
    if rgb == True:
        fil = imagen.copy()
        cont = 0
        while cont < 3:
            fil[:,:,cont] = median(imagen[:,:,cont],diamond(dureza))
            cont = cont +1
        if unsolocolor == True:
          orig = imagen.copy()
          red = imagen[:,:,0] == roj
          green = imagen[:,:,1] == ver
          blue = imagen[:,:,2] == azu
          parte = red == green
          parte = parte == blue
          contraparte = ~parte 
          seccion = fil.copy()
          resto = orig.copy()
          a = 0
          while a < 3:
              seccion[:,:,a]=seccion[:,:,a]*parte
              resto[:,:,a]=resto[:,:,a]*contraparte
              a=a+1
          final = resto+seccion
        else:
            final = fil
    else:
        final = median(imagen,diamond(dureza))
    return final