#A python script to reconstruct a 3D image

#Overview:
#   -Converts pixel coordinates into cartesian coordinates
#   -Converts cartesian coordinates into cylindrical coordinates
#   -Rotates by desired rotation
#   -Converts back into catesian
#   -Converts back into pixel coordinates

#Imports relevent libraries
import imageio
import numpy
import cv2


def pxl2cart(i,j,dim_x,dim_y):

    #Converts pixel coordinates to cartesian coordinates
    y = dim_y/2 -j
    x = i - dim_x/2

    return x,y

def cart2pxl(x,y,dim_x,dim_y):

    #Converts cartesian coordinates to pixel coordinates
    i = int(x + dim_x/2)
    j = int(dim_y/2 -y)

    return i,j


def rotation(i,j,dtheta,dim_x,dim_y):

    x,y = pxl2cart(i,j,dim_x,dim_y)

    r,theta = cv2.cartToPolar(x,y)

    theta[0]+=dtheta

    x,y = cv2.polarToCart(r[0],theta[0])

    i,j = cart2pxl(x,y,dim_x,dim_y)

    return i,j


def main():

    #Creates canvas and object to be rotated
    dim_x = 256
    dim_y = 256
    canvas = np.zeros(dim_x,dim_y)
    object = np.ones(256)

    #Creates theta variables
    dtheta = 0.1
    theta_ttl = int(2*(np.pi)/dtheta)

    #Rotates the object
    for angle_no in range(0,theta_ttl):
        theta = dtheta*angle_no

        for i in range(0,256):

            x,y = rotation(i,0,theta,dim_x,dim_y)
