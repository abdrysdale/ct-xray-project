The pyxlman program opperates in the following manor:

1) The user selects the button to rotate the platform and the program saves the coordinates of this button.
2) The user inputs the rotation time (how long to wait after clicking the button before searching again) and the number of images (so the program doesn't go on forever)
3) The program then acquires the rough coordinates of where to look (to speed up the search) by looking for the image 'region.png'
4) The user must then start the acquisition on the pixelman program and then press any key on the python terminal to begin the pyxlman program.
5) The program then searches the area found earlier until it detects the completed status image ('Capture.png')
6) Once the completed status image has been found the program clickes the rotation button.
7) It then does nothing for the rotation time to avoid multiple rotations to one completed image.
8) This process then repeats until all images have been taken.


To run the program.

1) Open IDLE (from the desktop)
2) Open the pyxleman.py file (on the desktop)
3) Click Run and then Run Module (or just F5)
4) Follow the onscreen instructions and make sure that the pixelman software and the OWIsoft program are both in view at all times.