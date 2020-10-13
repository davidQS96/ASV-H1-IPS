#Bibliotecas
from tkinter import * #Para GUI (filedialog, etc)
from tkinter import filedialog #Manejo de archivos
from PIL import ImageTk, Image #Manejo de imágenes
from skimage import color
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

#Esta funcion cambia imagen a usar a contraste original
def useRawContrast():   
    imagePI_original = cs.globalElems["image1"]
    histPI_original =cs.globalElems["histPI1"]
              
    imageLbl = cs.globalElems["imageLbl2"]
    histLbl = cs.globalElems["histLbl2"]

    imagePI = ImageTk.PhotoImage(imagePI_original)
    imageLbl.configure(image = imagePI)
    imageLbl.image = imagePI

    histPI = histPI_original
    histLbl.configure(image = histPI)
    histLbl.image = histPI

    cs.addNewGlobElem(imagePI_original, "afterContr")

#Esta funcion cambia imagen a usar a contraste maximizado
def useMaxContrast():
    pathStrVar = cs.globalElems["pathStrVar"]
    isColor = cs.globalElems["isColorFormat"]
    temp = fn.maxContraste(pathStrVar.get(), not isColor, 3)

    print((temp[0]*255).astype(np.uint8))

    newImage = Image.fromarray((temp[0] * 255).astype(np.uint8))
    
    newHist = Image.fromarray(temp[1])

    newHistSize = (round(newHist.size[0] * 0.6), round(newHist.size[1] * 0.6))
    newHist = newHist.resize(newHistSize, Image.ANTIALIAS)    
    
    imageLbl = cs.globalElems["imageLbl2"]
    histLbl = cs.globalElems["histLbl2"]

    imagePI = ImageTk.PhotoImage(newImage)
    imageLbl.configure(image = imagePI)
    imageLbl.image = imagePI

    histPI = ImageTk.PhotoImage(newHist)
    histLbl.configure(image = histPI)
    histLbl.image = histPI

    cs.addNewGlobElem(newImage, "afterContr")
    
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
    imagePI = ImageTk.PhotoImage(Image.open("Imágenes Prueba/vistaPrevia.png"))
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

        cs.addNewGlobElem(isColorFormat, "isColorFormat")

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
    isColorFormat = cs.globalElems["isColorFormat"]
    
    contrastWd = Toplevel(root)
    cs.addNewWindow(contrastWd, "contrastWd")    

    titleLbl = Label(contrastWd, text = "Tarea 1 - Principios de utilización del color")

    originalLbl = Label(contrastWd, text = "Imagen original:")

    prevFrame = Frame(contrastWd)#-------------------------
    
    imgSk = io.imread(pathStrVar.get())

    if(not isColorFormat):
        imgSk = color.gray2rgb(imgSk)

    imgHSV = color.rgb2hsv(imgSk)
    intensity = imgHSV[:,:,2] * 255     
    prevHist = Image.fromarray(fn.crearHistograma(imgSk))
    newHistSize = (round(prevHist.size[0] * 0.6), round(prevHist.size[1] * 0.6))
    prevHist = prevHist.resize(newHistSize, Image.ANTIALIAS)

    histPI1 = ImageTk.PhotoImage(prevHist)
    histLbl1 = Label(prevFrame, image = histPI1)
    histLbl1.image = histPI1 # keep a reference!

    image1 = Image.open(pathStrVar.get())
    imagePI1 = ImageTk.PhotoImage(image1)
    imageLbl1 = Label(prevFrame, image = imagePI1)
    imageLbl1.image = imagePI1 # keep a reference!    

    #------------------------------------------------------

    #Uso de funcion propia de clasificacion
    modifImg, hasColor, imgDim = fn.importar(pathStrVar.get())

    modifLbl = Label(contrastWd, text = "Imagen modificada:")


    nextFrame = Frame(contrastWd)#-------------------------
    
    histPI2 = ImageTk.PhotoImage(prevHist)
    histLbl2 = Label(nextFrame, image = histPI2)
    histLbl2.image = histPI2 # keep a reference!

    imagePI2 = ImageTk.PhotoImage(Image.open(pathStrVar.get()))
    imageLbl2 = Label(nextFrame, image = imagePI2)
    imageLbl2.image = imagePI2 # keep a reference!


    cs.addNewGlobElem(histPI1, "histPI1")
    cs.addNewGlobElem(histLbl1, "histLbl1")
    cs.addNewGlobElem(image1, "image1")
    cs.addNewGlobElem(imageLbl1, "imageLbl1")
    cs.addNewGlobElem(histPI2, "histPI2")
    cs.addNewGlobElem(histLbl2, "histLbl2")
    cs.addNewGlobElem(imagePI2, "imagePI2")
    cs.addNewGlobElem(imageLbl2, "imageLbl2")

    #------------------------------------------------------
    
    modifPI = ImageTk.PhotoImage(Image.fromarray(modifImg))
    modifImgLbl = Label(contrastWd, image = modifPI)
    modifImgLbl.image = modifPI # keep a reference!
    

    rawBtn = Button(contrastWd, text = "Usar imagen 'en bruto'", command = useRawContrast)
    maxContrBtn = Button(contrastWd, text = "Usar imagen con contraste máximo", command = useMaxContrast)

    backBtn = Button(contrastWd, text = "Volver", command = cs.showPrevWindow)
    nextBtn = Button(contrastWd, text = "Siguiente", command = menufiltrado)


    #Agrega Widgets a padre
    cs.addNewWidgetToCurr(titleLbl, "titleLbl")
    cs.addNewWidgetToCurr(originalLbl, "originalLbl")
    cs.addNewWidgetToCurr(prevFrame, "prevFrame")
    cs.addNewWidgetToCurr(modifLbl, "modifLbl")
    cs.addNewWidgetToCurr(nextFrame, "nextFrame")
    cs.addNewWidgetToCurr(rawBtn, "rawBtn")
    cs.addNewWidgetToCurr(maxContrBtn,"maxContrBtn")
    cs.addNewWidgetToCurr(backBtn, "backBtn")
    cs.addNewWidgetToCurr(nextBtn,"nextBtn")

    cs.currWindowSet.packAllChildren()

    #Realiza pack al hijos de frames
    histLbl1.pack(side = LEFT)
    imageLbl1.pack(side = RIGHT)
    histLbl2.pack(side = LEFT)
    imageLbl2.pack(side = RIGHT)


def menufiltrado():
    def mostrar():
        global filtrada
        a = sal.get()
        b = gaus.get()
        c = col.get()
        d = dur.get()
        r = 0
        g = 0
        bl = 0
        if c == 1:
            r = int(red.get())
            g = int(green.get())
            bl = int(blue.get())
        print (c,r,g,bl)
        if a == 1 and b == 1:
            print ("error")
        elif a == 1:
            filtrada = fn.filtrosalpimienta(modifImg,hasColor,d,c,r,g,bl)
            print ("a")
        elif b == 1:
            filtrada = fn.gaussiano(modifImg,hasColor,d,c,r,g,bl)
            print ("b")
        return filtrada
    pathStrVar = cs.globalElems["pathStrVar"]
    
    menufiltradoWd = Toplevel(root)
    cs.addNewWindow(menufiltradoWd, "menufiltradoWd")    

    titleLbl = Label(menufiltradoWd, text = "Tarea 1 - Principios de utilización del color")

    originalLbl = Label(menufiltradoWd, text = "Imagen original:")

    imgNext = cs.globalElems["afterContr"]
    modifImg = np.array(imgNext)
    hasColor = cs.globalElems["isColorFormat"]
    imagePI = ImageTk.PhotoImage(imgNext)
    imageLbl = Label(menufiltradoWd, image = imagePI)
    imageLbl.image = imagePI # keep a reference!

    #Casillas para funciones
    sal = IntVar()
    csal = Checkbutton(menufiltradoWd, text = "Filtro para ruido sal y pimienta", variable=sal)
    gaus = IntVar()
    cgaus = Checkbutton(menufiltradoWd, text = "Filtro para ruido gaussiano", variable=gaus)
    
    #Dureza
    dur = IntVar()
    cdur = Checkbutton(menufiltradoWd, text = "Filtrado elevado", variable=dur)
    
    #Selección de color
    col = IntVar()
    ccol = Checkbutton(menufiltradoWd, text = "Filtrar un color", variable=col)
    
    colcond = Label(menufiltradoWd, text = "Inserte el color a filtrar en RGB")
    cred = Label(menufiltradoWd, text = "Valor canal rojo")
    red = Entry(menufiltradoWd)
    cgreen = Label(menufiltradoWd, text = "Valor canal verde")
    green = Entry(menufiltradoWd)
    cblue = Label(menufiltradoWd, text = "Valor canal azul")
    blue = Entry(menufiltradoWd)
    

    maxContrBtn = Button(menufiltradoWd, text = "Filtar imagen", command = mostrar)

    backBtn = Button(menufiltradoWd, text = "Volver", command = cs.showPrevWindow)
    nextBtn = Button(menufiltradoWd, text = "Visualizar", command = filtersaltWindow)


    #Agrega Widgets a padre
    cs.addNewWidgetToCurr(titleLbl, "titleLbl")
    cs.addNewWidgetToCurr(originalLbl, "originalLbl")
    cs.addNewWidgetToCurr(imageLbl, "imageLbl")
    cs.addNewWidgetToCurr(csal, "csal")
    cs.addNewWidgetToCurr(cgaus, "cgaus")
    cs.addNewWidgetToCurr(cdur, "cdur")
    cs.addNewWidgetToCurr(ccol, "ccol")
    cs.addNewWidgetToCurr(colcond, "colcond")
    cs.addNewWidgetToCurr(cred, "cred")
    cs.addNewWidgetToCurr(red, "red")
    cs.addNewWidgetToCurr(cgreen, "cgreen")
    cs.addNewWidgetToCurr(green, "green")
    cs.addNewWidgetToCurr(cblue, "cblue")
    cs.addNewWidgetToCurr(blue, "blue")
    cs.addNewWidgetToCurr(maxContrBtn,"maxContrBtn")
    cs.addNewWidgetToCurr(backBtn, "backBtn")
    cs.addNewWidgetToCurr(nextBtn,"nextBtn")

    cs.currWindowSet.packAllChildren()
    


def filtersaltWindow():
    
    
    
    pathStrVar = cs.globalElems["pathStrVar"]
    
    filtersaltWd = Toplevel(root)
    cs.addNewWindow(filtersaltWd, "filtersaltWd")    

    titleLbl = Label(filtersaltWd, text = "Tarea 1 - Principios de utilización del color")

    #Uso de funcion propia de clasificacion
    modifImg, hasColor, imgDim = fn.importar(pathStrVar.get())
    
    modifLbl = Label(filtersaltWd, text = "Imagen modificada:")
    
    modifPI = ImageTk.PhotoImage(Image.fromarray(filtrada))
    modifImgLbl = Label(filtersaltWd, image = modifPI)
    modifImgLbl.image = modifPI # keep a reference!

    def guardar():
        io.imsave("Filtrada.jpg",filtrada)




    backBtn = Button(filtersaltWd, text = "Volver", command = cs.showPrevWindow)
    nextBtn = Button(filtersaltWd, text = "Guardar", command = guardar)
    

    #Agrega Widgets a padre
    cs.addNewWidgetToCurr(titleLbl, "titleLbl")
    cs.addNewWidgetToCurr(modifLbl, "modifLbl")
    cs.addNewWidgetToCurr(modifImgLbl, "modifImgLbl")
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














