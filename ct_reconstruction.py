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
from scipy import ndimage
import cv2
import matplotlib.pyplot as plt
from tkinter import Tk, Label, filedialog


def pxl2cart(i,dim_x,dim_y):

    #Converts pixel coordinates to cartesian coordinates
    x = i - dim_x/2

    #Only calculates x as y is always zero
    return x

def cart2pxl(x,y,dim_x,dim_y):

    #Converts cartesian coordinates to pixel coordinates
    i = int(x + dim_x/2)
    j = int(dim_y/2 -y)

    return i,j


def rotation(i,theta,dim_x,dim_y):

    x = pxl2cart(i,dim_x,dim_y)

    y=0 #For a 1d case as pxl2cart will be used for 2d senario

    r,theta_ary= cv2.cartToPolar(x,y) #can set angleInDegrees=True
    theta_ary[0]+= theta

    x,y = cv2.polarToCart(r[0],theta_ary[0])

    i,j = cart2pxl(x,y,dim_x,dim_y)

    return i,j

#Creates window and obtains stack
def init_window():

    #Initialises the window (GUI)
    window = Tk()
    window.title("Rotational Reconstruction")
    window.geometry('300x100')

    #Asks the user to select an image
    wtxt_select = Label(window, text='Please select an image.')
    wtxt_select.grid(column=0,row=0)
    window.update()


    #Opens the image
    str_object = filedialog.askopenfilename()
    img_object = io.imread(str_object)

    return img_object

def main():

    #Creates canvas and object to be rotated
    dim_x = 256
    dim_y = 256
    dim_z = 256
    canvas = np.zeros((dim_x,dim_y,dim_z))
    obj_stack = init_window()

    #Creates theta variables
    theta = np.linspace(0.,359.,360)
    len_theta = len(theta)

    #For each angle rotate the object
    for no_img in range(0,len_theta):
        theta_angle = theta[no_img]

        for x in range(dim_x-1,0,-1):  #For each pixel in the object, perform rotation

            i,j = rotation(x,theta_angle,dim_x,dim_y)   #Rotates object coords

            for z in range(0,dim_z):

                #Draws the image on the canvas
                canvas[j,z,i] = obj_stack[no_img,z,x]


    #Smooths the image
    canvas = ndimage.filters.median_filter(canvas,3)
    io.imsave('test.tif',canvas)
    plt.imshow(canvas[128,:,:]);plt.show()

main()
