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
from skimage import exposure
import os
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






#Funcion que devuelve una imagen e histograma de intensidad al aplicar un aumento de contraste
#direccion es la ruta relativa de la imagen
#esGris es un booleano si imagen esta en tonos de gris
#porciento es el porcentaje de brillo de los extremos del histograma que no se contemplan por el algoritmo
def maxContraste(direccion, esGris, porciento):

    if porciento < 0 or porciento > 10:
        return None #Deberia aparecer mensaje de error cuando devuelva None

    img = io.imread(direccion)

    if(esGris):
        img = color.gray2rgb(img)

    return maxContrasteAux(img, porciento)
    

#Esta funcion crea un histograma de intensidad de una imagen (HSI, tono de gris en caso de imagenes correspondientes)
#Devuelve el histograma en forma de numpy.ndarray
#img es la imagen con forma numpy.ndarray
#titulo es del histograma
#nombreArchivo es el nombre con el que se guardara
#aBorrar es verdadero si se quiere borrar el archivo generado
def crearHistograma(img, titulo = "Histograma de intensidad", nombreArchivo = "hist", aBorrar = True):
    histogram, bin_edges = numpy.histogram(img, bins = 256, range = (0, 255)) #calculating histogram

    #Ejes, titulos de ejes, rangos
    plt.figure()
    plt.title(titulo)
    plt.xlabel("Valor de intensidad")
    plt.ylabel("# Píxeles")
    plt.xlim([0, 255])  # <- named arguments do not work here

    plt.plot(bin_edges[0 : -1], histogram)

    path = "tempFiles/"+ nombreArchivo + ".png"
    
    plt.savefig(path) #Guarda un archivo en computadora

    temp = io.imread(path)

    if aBorrar:
        os.remove(path) #Se borra archivo en computadora, si se desea

    return temp



#Funcion auxiliar para maxContraste
#Genera el maximo de contraste que se quiera segun un porcentaje de 0 a 10%
#Devuelve el histograma de intensidad posterior y la imagen con maximo de color
#imgRGB es la imagen en formato RGB (3 canales)
#porciento es el porciento de brillo
def maxContrasteAux(imgRGB, porciento):
    imgHSV = color.rgb2hsv(imgRGB)  
    
    intensidad = imgHSV[:,:,2] * 255

    #https://numpy.org/doc/stable/reference/generated/numpy.percentile.html
    #https://scikit-image.org/docs/dev/auto_examples/color_exposure/plot_equalize.html
    
    #Se ordenan los datos y se obtienen los valores cuyas posiciones porcentuales se piden
    #El pi es el percentil inicial porciento%, mientras que pf es el percentil final (100-porciento)%
    pi, pf = numpy.percentile(intensidad, (porciento, 100 - porciento)) 

    #https://scikit-image.org/docs/dev/api/skimage.exposure.html?highlight=rescale_intensity#skimage.exposure.rescale_intensity
    #Esta funcion comprime o expande el rango de valores comprendidos entre pi y pf, sin rellenar valores intermedios de haber
    intModif = exposure.rescale_intensity(intensidad, in_range = (pi, pf))
    
    imgHSV[:,:,2] = intModif

    newRGB = color.hsv2rgb(imgHSV)

    histPost = crearHistograma(intModif * 255)

    return newRGB, histPost









    
    


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
