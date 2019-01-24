# A program that applies a set of preprocessing algorithms to a selection of images

#Libraries to download:
#   -numpy      (for general maths and array manipulation)
#       https://pypi.org/project/numpy/

#   -imageio    (for reading and writing images)
#       https://pypi.org/project/imageio/

#   -scipy      (for the preprocessing functions and general manipulation)
#       https://pypi.org/project/scipy/

#   -matplotlib (for image display)
#       https://pypi.org/project/matplotlib/


#Useful tutorial links:
#   http://www.scipy-lectures.org/advanced/image_processing/#geometrical-transformations
#   https://likegeeks.com/python-gui-examples-tkinter-tutorial/


#Bugs/Improvements:
#       -Dir separator different for windows and linux

# Imports relevent libraries
import numpy as np
import imageio
import os
from scipy import ndimage
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
def processor_algorithms(img_raw,img_flat,img_dark):

    #Tests if image is of the right dimensions
    dim_x,dim_y= img_raw.shape

    #Crops image
    if dim_x != 256 and dim_y != 256:

        #Assumes a constant boarder to crop image
        boarder =int(2 + (dim_x - 256)/2)
        img_raw = img_raw[boarder:256+boarder,boarder:256+boarder]


    #Performs flatfield correction:
    img_rtn = img_raw - img_dark
    img_raw = img_flat - img_dark   #Reuses img_raw for memory conservation
    img_raw[img_raw == 0] = 1       #Avoids dividing by zero
    img_rtn = np.divide(img_rtn,img_raw)
    img_rtn*=255

	#Returns the result as unsigned interger
    return img_rtn.astype('uint8')


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
	    window, text="                                     Thank you.                                     ")
	no_folder.grid(column=0, row=10)
	window.update()

	return dir_path

# Obtains just the file name from a whole path
def file_name(path):

	# Finds the starting index of the file
	for i in range(0, len(path)):
		if path[i] == "/":
			dir_index = i

	# Returns only the file name
	image_name = path[dir_index:len(path)]

	return image_name

def FFC_path_images():

    str_file = "FFC_image_paths.txt"

    #Creates file if doesn't exist
    if os.path.exists(str_file) == False:
        file = open(str_file,"w")
        file.close()

    #Reads image paths from file
    file = open(str_file,"r")
    str_flat_img = file.readline()
    str_dark_img = file.readline()
    index_nl= str_flat_img.find('\n')
    str_flat_img = str_flat_img[0:index_nl]


    #Acquires the flat field image from usr
    if os.path.exists(str_flat_img) == False:

        #Prompts usr to select image
        txt_FFC = Label(window, text="Please select the flat field image.")
        txt_FFC.grid(column=0,row=10)
        window.update()
        str_flat_img = filedialog.askopenfilename()

    #Acquires the dark count image
    if os.path.exists(str_dark_img) == False:

        #Prompts usr to select image
        txt_FFC = Label(window, text="Please select the dark count image.")
        txt_FFC.grid(column=0,row=10)
        window.update()
        str_dark_img = filedialog.askopenfilename()

    #Opens images
    img_flat = imageio.imread(str_flat_img,pilmode='L')
    img_dark = imageio.imread(str_dark_img,pilmode='L')

    #Writes correct image paths to file
    file.close()
    file = open(str_file,"w")
    str_write=str_flat_img+"\n"+str_dark_img
    file.write(str_write)
    file.close()

    return img_flat,img_dark

# Launches the application
def app_launch():

	# Initital variables
    continue_condition = True

	# Obtains the dir path to save photos
    #save_path = dir_save_path()
    #!--------------------------Change paths post testing (1)------------------!
    save_path = '/home/usr/Documents/Programs/ct-x-ray-project/Processed_images'

    img_flat,img_dark = FFC_path_images()

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
            save_name = save_path+"/"+image_name

            # Reads in the image as gray-scale (no colour information present)
            img = imageio.imread(image_path[i],pilmode='L')

            # Displays number of images remaing and updates progress bar
                # Displays how many images are remaining in correct english
            if (no_items-i) != 1:
                remain_txt = str(no_items-i)+" images remaining."
            else:
                remain_txt = "1 image remaining."

                # Updates number of remaining images
            img_remain = Label(window, text=remain_txt)
            img_remain.grid(column=0, row=20)

                # Updates progress bar
            percent = int(100*i/no_items)
            bar['value'] = percent
            window.update()

            # Filters image and performs brightness correction
            img = processor_algorithms(img,img_flat,img_dark)

            #Displays the image
            plt.imshow(img,cmap='gray')
            plt.show()

            # Saves the image
            imageio.imwrite(save_name, img)

		# Updates image remaining text and progress bar
        im_remain = Label(window, text="                     Done                     ")
        im_remain.grid(column=0, row=10)
        bar['value'] = 100
        window.update()

        # Asks to retry
        continue_condition = messagebox.askyesno('Continue?', 'Would you like to filter more images?')

    # Closes the program
    window.destroy()

# Launches the application
app_launch()
