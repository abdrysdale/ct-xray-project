#A python script to reconstruct a 3D image

#Overview:
#   -For each slice:
#       -Converts into cylindrical coordinates
#       -Rotates the image
#       -Converts into pixel coordinates
#       -Saves in 3D array
#   -Filters final image
#   -Displays a slice and saves 3D final image

#Imports relevent libraries
from skimage import io
import numpy as np
from scipy import ndimage as ndi
import skimage.transform as skt
import matplotlib.pyplot as plt
from tkinter import Tk, Label, filedialog,Button
from tkinter import *
from tkinter.ttk import Progressbar





#Initialises the window (GUI)
window = Tk()
window.title("Rotational Reconstruction")
window.geometry('400x100')

#Creates progress bar
bar = Progressbar(window, length=400)
bar.grid(column=0,row=10)


def get_image(window):

    #Asks the user to select an image
    wtxt_select = Label(window, text='Please select an image.')
    wtxt_select.grid(column=0,row=0)
    window.update()


    #Opens the image
    str_object = filedialog.askopenfilename()
    img_object = io.imread(str_object)

    #Thanks the user
    wtxt_select = Label(window, text="          Cheers.         ")
    wtxt_select.grid(column=0,row=0)
    window.update()

    return img_object

def main():

    #Acquires object from user and creates canvas for 3D image
    obj_stack = get_image(window)
    dim_stack = obj_stack.shape
    obj_fbp= np.zeros((dim_stack[1],dim_stack[1],dim_stack[1])) #As image is square

    #Creates slider for slice selection
    slider = Scale(window, from_=0, to=dim_stack[1]-1, orient=HORIZONTAL)
    slider.grid(column=0,row=30)
    window.update()

    #Creates theta array (in degrees)
    dtheta = 1
    theta = np.arange(0, dim_stack[0],dtheta)

    for i in range(0,dim_stack[1]):

        #Updates progress bar
        percentage = int(100*i/dim_stack[1])
        bar['value'] = percentage
        window.update()

        #Performs filtered back projection on each y slice
        obj_fbp[:,i,:] = skt.iradon(ndi.rotate(obj_stack[:,i,:],90),theta=theta,circle=True)

    #Saves the image
    io.imsave('test.tif',obj_fbp)

    #Button to display image
    #Displays new slice
    def clicked():
        plt.imshow(obj_fbp[:,slider.get(),:])
        plt.show()

    #Creates display button
    btn = Button(window, text="Load slice",bg="green",fg="white", command=clicked)
    btn.grid(column=0, row=20)
    window.update()

    window.mainloop()

main()
