#A program designed to rotate the rotation platform inbetween pixel man acquisions.


#Imports libraries
import pyautogui
import time
import os
import shutil


#Includes failsafe
pyautogui.FAILSAFE = True


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
            check_position = eval(input("Was this position correct?\nPress 1 for yes.\n"))
            if check_position == 1:
                happy = True

    #Clicks button
    def click(self):

        #Clicks button location
        pyautogui.click(x=self.position[0],y=self.position[1],button='left')

def main():

    #Image name pixelman in completed state
    im_name = 'Capture.png'

    #Acquires buttons
    rotation = button("Rotation")

    #Acquires time intervals
    rotation_time = eval(input("Please enter delay time in seconds\n"))
    angle_no = eval(input("Please enter the number of images being taken.\n"))

    #Coordinates with rotation inbetween image captures
    for i in range(0,angle_no):

        #Detects if pixelman has finished acquiring images
        while True:
            try:    #Trys to find image
                pos=len(list(pyautogui.locateAllOnScreen(im_name)))

            except: #If error then return pos = 0
                pos = 0

            if pos == 0: #If no object found then wait.
                time.sleep(0.1)
            else: #Breaks out of while loop if image has been found
                break


        #Rotates platform
        rotation.click()
        time.sleep(rotation_time)

    print("Done.")


#Launches the program
main()
