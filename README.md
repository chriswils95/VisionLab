# VisionLab
This repo contains all necessary files for detecting user similar faces, train an ai to do object detection and play around with computer vision on jetson nano and any computer.

# GETTING STARTED
pip is needed which is used to install all the necessary libraries. To install pip and setting up the virtual environment please [Follow this link](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

With the Virtual Environemnt setup and activated download the following libraries using pip install or sudo apt update:
* PIllow using pip install pillow
* cv2 using  pip3 install opencv-python or pip install opencv-python
* tkinter using sudo apt-get install python-tk on Ubuntu, or pip install python-tk on Windows and Mac
* pyqt5 using pip3 install --user pyqt5 
* face_recognition using pip install face_recognition
* pytorch following [this link](https://pytorch.org/get-started/locally/)

# RUN THE PROJECT
On the Terminal, navigate to the downloaded folder, cd into the Practice Directory and run the main_window.py scripts using python main_window.py

# PROJECT FUNCTIONALITIES
This project was built to allow students to be acquainted with artificial intelligence, and machine learning.

 # MAIN MENU
  The Main menu allows users to choose which application they want to practice on. Click on any of the listed menu or frames open up a new window. For the Project we focus on Computer vision, object detection and similarity face detection
![Alt Text](https://github.com/chriswils95/VisionLab/blob/master/images/Screenshot%20from%202020-08-17%2009-44-29.png)

# COMPUTER VISION PLAYGROUND
This playground allows user or students to play around with computer vision by setting hues, brightness, saturations etc.
* NOTE: Switching from the main window to the computer vision window takes like 5 seconds, this is due to the fact that the main window and vision window were written in different gui libraries
![Alt Text](https://github.com/chriswils95/VisionLab/blob/master/images/Screenshot%20from%202020-08-17%2009-49-08.png)

# SIMILARITY FACE DETECTION
This playground allows users or students to match their face with faces of church leaders. To start the application click the start button. Clicking the start buttons allows the program to go through the pre-trained face models of all the church leaders and matches yours with the one with the closest confidence interval.
Sto button stop the programs and the face evaluation, and the clear button clears the buttons colors and resets any counters.
![Alt Text](https://github.com/chriswils95/VisionLab/blob/master/images/Screenshot%20from%202020-08-17%2009-49-08.png)


