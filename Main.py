#Bibliotecas
from tkinter import * #Para GUI (filedialog, etc)
from tkinter import filedialog #Manejo de archivos
from PIL import ImageTk, Image #Manejo de imágenes
import os

#-------------------------------------------------------
#Constantes

#-------------------------------------------------------
#Funciones

#Función que muestra al usuario una ventana de búsqueda de archivos y asigna a resultStr el directorio donde se encuentra una imagen válida
#resultStr es un tkinter.StringVar()
def browseImgFile(resultStr):
    
    #https://stackoverflow.com/questions/19944712/browse-for-file-path-in-python
    currdir = os.getcwd()

    #https://docs.python.org/3.9/library/dialog.html
    tempdir = filedialog.askopenfilename(parent=root, initialdir = currdir, title = 'Seleccione un archivo de imagen') #Ventana emergente

    #https://www.thetopsites.net/article/53470882.shtml
    if len(tempdir) > 0 and tempdir.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')): #Archivos de imagen soportados
        resultStr.set(tempdir) #Asigna la imagen válida que se encontró

    else:
        print("Archivo no valido")        

    return

#-------------------------------------------------------
#Clases

class CurrentState:

    def __init__(self):
        self.currRelImgPath = 2






#-------------------------------------------------------
#Programa principal


##Mostrar tamano, 
def mainScreen():
    #https://www.youtube.com/watch?v=YXPyB4XeYLA&ab_channel=freeCodeCamp.org
    titleLbl = Label(root, text = "Tarea 1 - Principios de utilización del color")
    pathStrVar = StringVar()

    filePathLbl = Label(root, textvariable = pathStrVar)
    browseBtn = Button(root, text = "Buscar imagen", command = lambda: browseImgFile(pathStrVar))
    nextBtn = Button(root, text = "Siguiente")

    #http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
    imagePI = ImageTk.PhotoImage(Image.open("Imágenes Prueba/paisajeBW2.jpg"))
    imageLbl = Label(image = imagePI)
    imageLbl.image = imagePI # keep a reference!
    

    titleLbl.pack()
    imageLbl.pack()
    filePathLbl.pack()
    browseBtn.pack()
    nextBtn.pack()

    

def clasifScreen():
    return
    
    

root = Tk()
mainScreen()
root.mainloop()














