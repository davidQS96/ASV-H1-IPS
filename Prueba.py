from tkinter import*
from PIL import ImageTk, Image

root = Tk()



imagePI = ImageTk.PhotoImage(Image.open("lowContrast.png")) #Devolver a "Imágenes Prueba/vistaPrevia.png"
imageLbl = Label(root, image = imagePI)
imageLbl.image = imagePI # keep a reference!


imageLbl.pack()


#Comienza loop para mantener GUI
root.mainloop()
