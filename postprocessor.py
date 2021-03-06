# A program that applies a set of postprocessing algorithms to a selection of images

#Libraries to download:
#   -numpy      (for general maths and array manipulation)
#       https://pypi.org/project/numpy/

#   -skimage (for reading and writing images)
#       https://pypi.org/project/skimage/

#   -matplotlib (for image display)
#       https://pypi.org/project/matplotlib/


#Useful tutorial links:
#   http://www.scipy-lectures.org/advanced/image_processing/#geometrical-transformations
#   https://likegeeks.com/python-gui-examples-tkinter-tutorial/


# Imports relevent libraries
import numpy as np
from skimage import io
from scipy import ndimage as ndi
import os
import matplotlib.pyplot as plt
from tkinter import Tk, Label, messagebox, ttk, filedialog
from tkinter.ttk import Progressbar


# Initialises window with a title and set dimensions
window = Tk()
window.title("Preprocessor")
window.geometry('500x500')


# Creates a progress bar
bar = Progressbar(window, length=300)
bar.grid(column=0, row=0)


# Performs the necessary preprocessing algorithms
def processor_algorithms(img_raw,img_flat):

    #Initial variables
    fltr_rad = 1
    hard_fltr_rad = 10

    #Performs flatfield correction:
    img_flat[img_flat == 0] = 1       #Avoids dividing by zero
    m  = np.mean(img_raw)             #Calculates average for scaling
    img_rtn = np.divide(img_raw,img_flat)
    img_rtn*=m

    #Performs a soft median filter
    img_rtn = ndi.filters.median_filter(img_rtn,size=fltr_rad)

    #Harder median filter on masked pixels
    img_hard_filter = ndi.filters.median_filter(img_rtn,size=hard_fltr_rad)
    img_rtn[img_flat == 1] = img_hard_filter[img_flat == 1]

	#Returns the result
    return img_rtn


# Obtains the folder for the processed images to be saved to
def dir_save_path():

	# Asks user to select a save location
	no_folder = Label(window, text="Please select a folder to save the processed images.")
	no_folder.grid(column=0, row=10)
	window.update()

	# Obtains the user selected folder
	dir_path = filedialog.askdirectory()

	# Informs user of update
	no_folder = Label(
	    window, text="                                     Thank you.                                    ")
	no_folder.grid(column=0, row=10)
	window.update()

	return dir_path

# Obtains just the file name from a whole path
def file_name(path):

	# File separator for cross-platform compatability
    sep = os.sep

    #Finds the starting index of the file
    for i in range(0, len(path)):
        if path[i] == sep:
            dir_index = i

	# Returns only the file name
    image_name = path[dir_index:len(path)]

    return image_name

def FFC_path_images():

    #Prompts usr to select image
    txt_FFC = Label(window, text="Please select the flat field image.")
    txt_FFC.grid(column=0,row=10)
    window.update()
    str_flat_img = filedialog.askopenfilename()


    #Opens image
    img_flat = io.imread(str_flat_img)

    return img_flat

# Launches the application
def app_launch():

	# Initital variables
    continue_condition = True
    sep = os.sep

	# Obtains the dir path to save photos
    save_path = dir_save_path()

    #Obtains flat field image
    img_flat = FFC_path_images()

    while (continue_condition == True):

        # User prompted to select image(s) for filtering
        txt_img_select = Label(window, text="Please select the image(s) to be processed.")
        txt_img_select.grid(column=0,row=10)
        window.update()
        image_path = filedialog.askopenfilenames()
        no_items = len(image_path)

		# Processes and saves all selected images
        for i in range(0, no_items):

			# Obtains the image name and creates the path for the image to be saved to
            image_name = file_name(image_path[i])
            save_name = save_path+sep+image_name

            # Reads in the image
            img = io.imread(image_path[i])

            #Iterates over the dimensions
            dim = img.shape

            if len(dim) == 2:
                z = 1
            else:
                z = dim[0]
                img_rtn = np.zeros(dim)

            # Displays number of images remaing and updates progress bar
            # Displays how many images are remaining in correct english
            for slice in range(0,z):
                if (no_items-i) != 1:
                    remain_txt = str(no_items-i)+" images remaining."
                else:
                    remain_txt = "1 image remaining."

                # Updates number of remaining images
                img_remain = Label(window, text=remain_txt)
                img_remain.grid(column=0, row=20)

                # Updates progress bar
                percent = int(100*slice/z)
                bar['value'] = percent
                window.update()


                # Filters image and performs brightness correction
                if z != 1:
                    img_rtn[slice,:,:] = processor_algorithms(img[slice,:,:],img_flat)
                else:
                    img_rtn = processor_algorithms(img,img_flat)

            # Saves the image
            io.imsave(save_name, img_rtn.astype('uint16'), plugin='tifffile')

		# Updates image remaining text and progress bar
        im_remain = Label(window, text="                     Done                     ")
        im_remain.grid(column=0, row=10)
        bar['value'] = 100
        window.update()

        #Plots image, processed image and difference
        _,axes=plt.subplots(2,2)
        plt.subplots_adjust(left=0, bottom=0, right=1, top=1, wspace=0, hspace=0)

        if z != 1:
            axes[0,0].imshow(img[slice,:,:],cmap='gray')
            axes[0,1].imshow(img_rtn[slice,:,:],cmap='gray')
            img_sub=img_rtn - img
            axes[1,0].imshow(img_sub[slice,:,:],cmap='gray')
            axes[1,1].imshow(img_flat,cmap='gray')

        else:
            axes[0,0].imshow(img,cmap='gray')
            axes[0,1].imshow(img_rtn,cmap='gray')
            img_sub=img_rtn - img
            axes[1,0].imshow(img_sub,cmap='gray')
            axes[1,1].imshow(img_flat,cmap='gray')
        plt.show()

        # Asks to retry
        continue_condition = messagebox.askyesno('Continue?', 'Would you like to filter more images?')

    # Closes the program
    window.destroy()

# Launches the application
app_launch()
