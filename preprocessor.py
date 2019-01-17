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

# Imports relevent libraries
import numpy as np
import imageio
from scipy import misc,ndimage
import matplotlib.pyplot as plt
from tkinter import Tk, Label, messagebox, ttk, filedialog
from tkinter.ttk import Progressbar


# Initialises window with a title and set dimensions
window = Tk()
window.title("Preprocessor")
window.geometry('350x100')


# Creates a progress bar
prog_length = 350
bar = Progressbar(window, length=prog_length)
bar.grid(column=0, row=0)


# Performs the necessary preprocessing algorithms
def processor_algorithms(img):

    # Performs a guassian blur
    img_rtn = ndimage.gaussian_filter(img, sigma=3)

	# Returns the result
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

# Launches the application


def app_launch():

	# Initital variables
    continue_condition = True

	# Obtains the dir path to save photos
    save_path = dir_save_path()
    
    while (continue_condition == True):

        # User prompted to select image(s) for filtering
        image_path = filedialog.askopenfilenames()
        no_items = len(image_path)

		# Processes and saves all selected images
        for i in range(0, no_items):

			# Obtains the image name and creates the path for the image to be saved to
            image_name = file_name(image_path[i])
            save_name = save_path+"\\"+image_name

            # Reads in the image
            img = imageio.imread(image_path[i])

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
            img = processor_algorithms(img)

            # Saves the image
            imageio.imwrite(save_name, img)

		# Updates image remaining text and progress bar
        im_remain = Label(window, text="                  Done                  ")
        im_remain.grid(column=0, row=10)
        bar['value'] = 100
        window.update()

        # Asks to retry
        continue_condition = messagebox.askyesno('Continue?', 'Would you like to filter more images?')

    # Closes the program
    window.destroy()

# Launches the application
app_launch()
