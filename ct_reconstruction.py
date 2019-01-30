#A python script to reconstruct a 3D image

#Overview:
#   -Converts pixel coordinates into cartesian coordinates
#   -Converts cartesian coordinates into cylindrical coordinates
#   -Rotates by desired rotation
#   -Converts back into catesian
#   -Converts back into pixel coordinates

#Imports relevent libraries
import imageio
import numpy as np
import cv2
import matplotlib.pyplot as plt


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


def main():

    #Creates canvas and object to be rotated
    dim_x = 256
    dim_y = 256
    canvas = np.zeros((dim_x,dim_y))
    obj_line = np.concatenate((np.zeros(120),np.ones(16),np.zeros(120)))

    #Creates theta variables
    dtheta = 0.001
    theta_ttl = int(2*(np.pi)/dtheta)

    #For each angle rotate the object
    for angle_no in range(0,theta_ttl):
        theta = dtheta*angle_no

        for x in range(255,0,-1):  #For each pixel in the object, perform rotation

            i,j = rotation(x,theta,dim_x,dim_y)   #Rotates object coords

            canvas[j,i] = obj_line[x]             #Draws object value on canvas

    plt.imshow(canvas)
    plt.show()

main()
