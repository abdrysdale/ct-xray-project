#A python script to reconstruct a 3D image

#Overview:
#   -Uses a filtered back projection on each sinogram and saves as a stack
#   -Displays the results

#Imports relevent libraries
from skimage import io
import numpy as np
import os
from scipy import ndimage as ndi
import skimage.transform as skt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import Tk, Label, filedialog
from tkinter import *
from tkinter.ttk import Progressbar


#Initialises the window (GUI)
window = Tk()
window.title("Filtered Back Projection")
window.geometry('400x400')

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

    return img_object,str_object

#Obtains the folder for the filtered images to be saved to
def dir_save_path():

	#Opens the file containg the save path
	save_path="save_path.txt"

	#Creates the text file if non-existent
	if os.path.exists(save_path)==False:
		file=open(save_path,"w")
		file.close()

	#Opens the file to read in the save dir name
	file=open(save_path,"r")
	dir_path=file.readline()

	#Asks the user to select the folder if one is not pre saved
	if os.path.isdir(dir_path)==False:

		#Asks user to select a save location
		no_folder=Label(window,text="Please a save folder.")
		no_folder.grid(column=0,row=0)
		window.update()

		#Obtains the user selected folder
		dir_path=filedialog.askdirectory()

		#Informs user of update
		no_folder=Label(window, text="           Ta.            ")
		no_folder.grid(column=0,row=0)
		window.update()

	#Writes the result to the save_path file
	file.close()
	file=open(save_path,"w")
	file.write(dir_path)
	file.close()

	return dir_path

#Obtains just the file name from a whole path
def file_name(path):

	#Finds the starting index of the file
	for i in range(0,len(path)):
		if path[i]=="/":
			dir_index=i

	#Returns only the file name
	image_name=path[dir_index+1:len(path)]
	return image_name

def main():

    #Acquires object from user and creates black object for filtered back projection
    obj_stack,str_object = get_image(window)
    dim_stack = obj_stack.shape
    obj_fbp= np.zeros((dim_stack[1],dim_stack[1],dim_stack[1])) #As image is square dimensions are the same

    #Gets save location
    dir_save = dir_save_path()
    str_imname = file_name(str_object)
    str_save = os.path.join(dir_save, str_imname)

    #Creates theta array (in degrees)
    dtheta = 1
    theta = np.arange(0, dim_stack[0],dtheta)

    #Redefining dot calls
    iradon = skt.iradon
    rotate = ndi.rotate

    #Obtains reconstruction using filtered back projection
    for i in range(0,dim_stack[1]):

        #Updates progress bar
        percentage = int(100*i/dim_stack[1]+1)
        bar['value'] = percentage
        window.update()


        #Performs filtered back projection on each y slice
        obj_fbp[i,:,:] = iradon(rotate(obj_stack[:,i,:],90),theta=theta,circle=True,filter='ramp', interpolation='linear')

    #Saves the image
    print(dir_save+"\n"+str_imname +"\n"+str_save)
    io.imsave(str_save,obj_fbp.astype('int16'),plugin='tifffile')

    #Plots the figure
    fig = Figure(figsize=(3,3))
    a = fig.add_subplot(111)
    a.imshow(obj_fbp[0,:,:])

    #Draws to tkinter
    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().grid(row=60,column=0)
    canvas.draw()

    #Updates image command
    def slider_moved(val):
        a.clear()
        a.imshow(obj_fbp[int(val),:,:])
        canvas.draw()

    #Adds slider to select plane
    slider = Scale(window,from_=0, to=dim_stack[1]-1,orient=HORIZONTAL,command=slider_moved)
    slider.grid(row=30,column=0)

    window.mainloop()

main()
