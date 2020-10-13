#Bibliotecas
from tkinter import * #Para GUI (filedialog, etc)
from tkinter import filedialog #Manejo de archivos
from PIL import ImageTk, Image #Manejo de imágenes
import numpy as np
import os

import Functions as fn

#-------------------------------------------------------
#Constantes

#-------------------------------------------------------
#Funciones

#Función que muestra al usuario una ventana de búsqueda de archivos y asigna a pathStrVar el directorio donde se encuentra una imagen válida
#Despues actualiza la imagen dentro de GUI
#pathStrVar es un tkinter.StringVar()
#imagePI es un tkinter.PhotoImage
#imageLbl es un tkinter.Label usado para colocar la imagen
def browseImgFile():
    errorStrVar = cs.getElemFromCurr("errorStrVar") 
    
    currdir = os.getcwd()   

    try:
        #https://docs.python.org/3.9/library/dialog.html
        tempdir = filedialog.askopenfilename(parent = root, initialdir = currdir, title = 'Seleccione un archivo de imagen') #Ventana emergente
        #https://www.thetopsites.net/article/53470882.shtml
        
        if len(tempdir) > 0 and tempdir.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')): #Archivos de imagen soportados
            pathStrVar = cs.globalElems["pathStrVar"]
            pathStrVar.set(tempdir) #Asigna la imagen válida que se encontró
            
            errorStrVar.set("")

            imagePI = cs.getElemFromCurr("imagePI")
            
            imageLbl = cs.getWidgFromCurr("imageLbl")

            #https://stackoverflow.com/questions/3482081/how-to-update-the-image-of-a-tkinter-label-widget
            imagePI = ImageTk.PhotoImage(Image.open(tempdir))
            imageLbl.configure(image = imagePI)
            imageLbl.image = imagePI

        else:
            #Muestra mensaje de error en caso de que no se elija un archivo adecuado
            errorStrVar.set("Archivo no válido, elija uno soportado por el programa (.png, .jpg, .jpeg, .tiff, .bmp, .gif)")
            print("Archivo no valido")

    except:
        errorStrVar.set("Archivo no válido, elija uno soportado por el programa (.png, .jpg, .jpeg, .tiff, .bmp, .gif)")
        print("Se cerro ventana")

    return

#-------------------------------------------------------
#Clases

#Esta clase se usa para mantener información a través de la progresión del programa
class CurrentState:

    #Método constructor
    def __init__(self):
        self.windowStack = {} #Lista de objetos ventana con estructura de stack (First in, Last out)
        self.numWindows = 0

        self.currWindowSet = None

        self.globalElems = {} #Lista/diccionarios con elementos que se usan en todo el programa


    #Método que agrega una ventana en el stack del programa
    #newScreen es un objeto Tk() o Toplevel()
    def addNewWindow(self, newWindow, windowName):        
        
        if(self.numWindows > 0): #Si hay una ventana que se pueda ocultar
            self.getLastStackElement().window.withdraw() #Oculta ventana anterior

        self.currWindowSet = WindowSet(newWindow, windowName)

        self.addToStack(self.currWindowSet, windowName)

    #Método que agrega un elemento global
    def addNewGlobElem(self, newElem, elemName):
        self.globalElems[elemName] = newElem 

        
    #Metodo para agregar un widget a la lista de la ventana actual
    def addNewWidgetToCurr(self, newWidget, widgetName):
        self.currWindowSet.addWidgetChild(newWidget, widgetName)


    #Metodo para obtener un widget de la ventana actual
    def getWidgFromCurr(self, widgetKey):
        return self.currWindowSet.childPackOrder[widgetKey]


    #Metodo para obtener un elemento no-widget de la ventana actual
    def getElemFromCurr(self, elemKey):
        return self.currWindowSet.otherElements[elemKey]


    #Metodo para agregar un no-widget a la lista de la ventana actual
    def addNewElemToCurr(self, newElem, elem):
        self.currWindowSet.addNonWidgChild(newElem, elem)
        

    #Metodo que muestra unicamente ventana anterior en stack, y destruye ventanas posteriores
    def showPrevWindow(self):
        if(self.numWindows > 1): #Verifica que hayan ventanas que se puedan remover, si =1, solo se tiene root            
            tempWd = self.removeFromStack()
            self.currWindowSet = self.getLastStackElement()
            self.currWindowSet.window.deiconify()
            tempWd.destroy()
            

    #Agrega nuevo elem al stack
    def addToStack(self, newElement, objectKey):
        self.windowStack[objectKey] = newElement 

        self.numWindows += 1
        

    #Metodo que remueve y retorna ultimo elem en stack.
    #Si no hay items en windowStack, devuelve nulo
    def removeFromStack(self):
        temp = None

        if(self.numWindows > 0):
            temp = self.windowStack.popitem()[-1] #Remueve ultimo elem del stack
            self.numWindows -= 1

        return temp
    
    
    #Metodo que retorna ultima ventana objeto de lista
    def getLastStackElement(self):
        temp = self.windowsToList()
        return temp[-1]


    #Metodo que devuelve los elementos del diccionario como una lista, sin las llaves
    def windowsToList(self):
        return list(self.windowStack.values())


#Clase para agrupar ventana y widgets hijos, junto con informacion de cada uno
#Esta clase sirve principalmente para organizar clase CurrentState
class WindowSet:

    #Metodo constructor
    def __init__(self, window ,windowName):
        self.name = windowName
        self.window = window

        self.childPackOrder = {}
        self.otherElements = {}


    #Metodo destructor
    def __del__(self):
        self.window.destroy()
        

    #Metodo para asegurarse de eliminar ventana
    def destroy(self):
        self.__del__()


    #Agrega widget hijo a diccionario
    def addWidgetChild(self, widget, widgetName):
        self.childPackOrder[widgetName] = widget
        

    #Agrega hijo no-widget a diccionario
    def addNonWidgChild(self, elem, elemName):
        self.otherElements[elemName] = elem
        

    #Realiza pack() a todos los hijos de ventana, en el orden en el que se agregaron
    def packAllChildren(self):
        tempItems = list(self.childPackOrder.values())

        for item in tempItems:
            item.pack()

#-------------------------------------------------------
#Programa principal

#Esta función muestra la ventana inicial del programa 
def mainWindow():

    titleLbl = Label(root, text = cs.globalElems["titulo"])
    pathStrVar = StringVar()
    cs.addNewGlobElem(pathStrVar, "pathStrVar")

    #http://effbot.org/pyfaq/why-do-my-tkinter-images-not-appear.htm
    #https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-tkinter-python#:~:text=To%20display%20images%20in%20labels,is%20present%20in%20tkinter%20package.&text=%22PhotoImage()%22%20function%20returns%20the%20image%20object.&text=To%20display%20image%20in%20Python,GIF%20and%20PGM%2FPPM%20formats.
    imagePI = ImageTk.PhotoImage(Image.open("paisajeRGB2.jpg")) #Devolver a "Imágenes Prueba/vistaPrevia.png"
    print(np.array(Image.open("paisajeRGB2.jpg")))
    pathStrVar.set("paisajeRGB2.jpg") #Borrar
    imageLbl = Label(root, image = imagePI)
    imageLbl.image = imagePI # keep a reference!

    #Widgets y similares
    filePathLbl = Label(root, textvariable = pathStrVar)
    browseBtn = Button(root, text = "Buscar imagen", command = browseImgFile)
    nextBtn = Button(root, text = "Siguiente", command = clasifWindow)
    errorStrVar = StringVar("")
    errorLbl = Label(root, textvariable = errorStrVar)

    #Agrega Widgets a padre
    cs.addNewWidgetToCurr(titleLbl, "titleLbl")
    cs.addNewWidgetToCurr(imageLbl,"imageLbl")
    cs.addNewWidgetToCurr(filePathLbl,"filePathLbl")
    cs.addNewWidgetToCurr(browseBtn,"browseBtn")
    cs.addNewWidgetToCurr(nextBtn,"nextBtn")
    cs.addNewWidgetToCurr(errorLbl,"errorLbl")

    cs.addNewElemToCurr(pathStrVar, "pathStrVar")
    cs.addNewElemToCurr(imagePI, "imagePI")
    cs.addNewElemToCurr(errorStrVar,"errorStrVar")

    #Coloca widgets en pantalla
    cs.currWindowSet.packAllChildren()

#clasifWindow clasifica la imagen, y la convierte a formatos de tono de gris de ser necesario      
def clasifWindow():

    #Muestra mensaje de error si no se ha elegido imagen aun
    pathStrVar = cs.globalElems["pathStrVar"]
    if(pathStrVar.get() == ""):
        errorStrVar = cs.getElemFromCurr("errorStrVar")
        errorStrVar.set("Elija primero una imagen")

    else:
        clasifWd = Toplevel(root)
        cs.addNewWindow(clasifWd, "clasifWd")

        #Widgets y similares
        titleLbl = Label(clasifWd, text = "Tarea 1 - Principios de utilización del color")

        originalLbl = Label(clasifWd, text = "Imagen original:")

        imagePI = ImageTk.PhotoImage(Image.open(pathStrVar.get()))
        imageLbl = Label(clasifWd, image = imagePI)
        imageLbl.image = imagePI # keep a reference!

        #Uso de funcion propia de clasificacion
        modifImg, isColorFormat, imgDim = fn.importar(pathStrVar.get())

        clasifText = ""
        
        if(isColorFormat):
            clasifText = "Clasificación: imagen en formato de color (se cambiará a formato en tonos de grises)."
        else:
            clasifText = "Clasificación: imagen en tonos de gris."

        clasifLbl = Label(clasifWd, text = clasifText)

        backBtn = Button(clasifWd, text = "Volver", command = cs.showPrevWindow)
        nextBtn = Button(clasifWd, text = "Siguiente", command = contrastWindow)

        #Agrega Widgets a padre
        cs.addNewWidgetToCurr(titleLbl, "titleLbl")
        cs.addNewWidgetToCurr(originalLbl, "originalLbl")
        cs.addNewWidgetToCurr(imageLbl, "imageLbl")
        cs.addNewWidgetToCurr(clasifLbl, "clasifLbl")
        cs.addNewWidgetToCurr(backBtn, "backBtn")
        cs.addNewWidgetToCurr(nextBtn,"nextBtn")

        cs.addNewElemToCurr(imagePI, "imagePI")

        #Coloca widgets en pantalla
        cs.currWindowSet.packAllChildren()

def contrastWindow():

    pathStrVar = cs.globalElems["pathStrVar"]
    
    contrastWd = Toplevel(root)
    cs.addNewWindow(contrastWd, "contrastWd")    

    titleLbl = Label(contrastWd, text = "Tarea 1 - Principios de utilización del color")

    originalLbl = Label(contrastWd, text = "Imagen original:")

    imagePI = ImageTk.PhotoImage(Image.open(pathStrVar.get()))
    imageLbl = Label(contrastWd, image = imagePI)
    imageLbl.image = imagePI # keep a reference!

    #Uso de funcion propia de clasificacion
    modifImg, hasColor, imgDim = fn.importar(pathStrVar.get())

    modifLbl = Label(contrastWd, text = "Imagen modificada:")
    
    modifPI = ImageTk.PhotoImage(Image.fromarray(modifImg))
    modifImgLbl = Label(contrastWd, image = modifPI)
    modifImgLbl.image = modifPI # keep a reference!
    

    rawBtn = Button(contrastWd, text = "Usar imagen 'en bruto'")
    maxContrBtn = Button(contrastWd, text = "Usar imagen con contraste máximo")

    backBtn = Button(contrastWd, text = "Volver", command = cs.showPrevWindow)
    nextBtn = Button(contrastWd, text = "Siguiente")


    #Agrega Widgets a padre
    cs.addNewWidgetToCurr(titleLbl, "titleLbl")
    cs.addNewWidgetToCurr(originalLbl, "originalLbl")
    cs.addNewWidgetToCurr(imageLbl, "imageLbl")
    cs.addNewWidgetToCurr(modifLbl, "modifLbl")
    cs.addNewWidgetToCurr(modifImgLbl, "modifImgLbl")
    cs.addNewWidgetToCurr(rawBtn, "rawBtn")
    cs.addNewWidgetToCurr(maxContrBtn,"maxContrBtn")
    cs.addNewWidgetToCurr(backBtn, "backBtn")
    cs.addNewWidgetToCurr(nextBtn,"nextBtn")

    cs.currWindowSet.packAllChildren()

   







    

#Pantalla raíz
root = Tk()

#Crea instancia global de CurrentState y guarda root
cs = CurrentState()
cs.addNewWindow(root, "root")
cs.addNewGlobElem("Tarea 1 - Principios de utilización del color", "titulo")

#Se abre pantalla inicial
mainWindow()

#Comienza loop para mantener GUI
root.mainloop()














