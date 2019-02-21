#A program designed to rotate the rotation platform inbetween pixel man acquisions.


#Imports libraries
import pyautogui
import time
import os
import shutil


#Includes failsafe
pyautogui.FAILSAFE = True

#Defines the button class for clicking
class button:

    #Gets initial button position
    def __init__(self,name):

        #Ensures loops until button location is correct
        happy = False
        while happy == False:

            #Prompts user to hover mouse over button
            print(("Please hover the mouse over the %s button" % name) )
            time.sleep(1)
            print("Location will be aquired in 5s")

            #Countdown for user
            for i in range(5,0,-1):

                print(i)
                time.sleep(1)

            #Acquires position of button
            x,y = pyautogui.position()
            print("Button position acquired.")
            self.position = (x,y)

            #Checks position with user
            pyautogui.moveTo(10,10,duration=0)
            pyautogui.moveTo(x, y, duration=2)
            check_position = eval(input("Was this position correct?\nPress 1 for yes or 0 for no.\n"))
            if check_position == 1:
                happy = True

    #Clicks button
    def click(self):

        #Clicks button location
        pyautogui.click(x=self.position[0],y=self.position[1],button='left')

#Acquires the search region
def get_region(reg_name):

    #Acquires search reqion of nearby object
    box = pyautogui.locateOnScreen(reg_name)

    #Converts to correct search coordinates
    coords = (box[0],box[1],box[2]*3,box[3])

    return coords


def main():

    #Image name pixelman in completed state
    im_name = 'Capture.png'
    reg_name = 'region.png'

    #Acquires buttons
    rotation = button("Rotation")

    #Acquires time intervals
    rotation_time = eval(input("Please enter delay time in seconds\n"))
    angle_no = eval(input("Please enter the number of images being taken.\n"))

    #Acquires the search region for completed status
    coords = get_region(reg_name)

    #User queues start time
    start = input("Press any key to start.\n")

    #Coordinates with rotation inbetween image captures
    for i in range(0,angle_no):

        #Detects if pixelman has finished acquiring images
        while True:
            try:    #Trys to find image
                pos=len(list(pyautogui.locateAllOnScreen(im_name,region=(coords[0],coords[1],coords[2],coords[3]))))

            except: #If error then return pos = 0
                pos = 0

            if pos != 0: #Breaks loop if object found
                break


        #Rotates platform
        rotation.click()
        print("Rotated image %d" % int(i+1))
        time.sleep(rotation_time)


    #Prints done
    print("Done.")


#Launches the program
main()
