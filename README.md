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

# NOTE
Change the self.spath variable to the path of church_leaders directory in your computer


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
![Alt Text](https://github.com/chriswils95/VisionLab/blob/master/images/Screenshot%20from%202020-08-17%2009-46-18.png)

# OBJECT DETECTION
This model allows users or students to train an ai to do object detection. As for now it is only limited to face detection, thumbs up and thumbs down detection.
![Alt Text](https://github.com/chriswils95/VisionLab/blob/master/images/Screenshot%20from%202020-08-17%2009-46-33.png)
* FACE DETECTION
  * Directions
   * Under the dataset drop down menu select face, type in your name or any name on the face name text box, position your face properly in front of the camera and       make sure you are in a bright environment. Click on the add button which captures your face from the camera and stores it in a directory. Make sure to add as much images as possible to have a more accurate result. After you are satisfied with your datasets click the train button which trains the AI to detect your face. Clicking the evaluate button, allows the AI to detect faces and display names of the faces, if your face is detected it will display your name and put a rectangle box on the detected face, else it will just say unknown.
* THUMBS DIRECTION DETECTION
  * Directions
  * Under the dataset drop down menu select thumbs, and select thumbs up or thumbs down on the category drop down depending on what you want to train first, direction your thumbs in front of the camera in the direction of the category selected and make sure you are in a bright environment. Click on the add button which captures your thumbs from the camera and stores it in a directory. Make sure to add as much images as possible to have a more accurate result, do the same thing for the other category. After you are satisfied with your datasets click the train button which trains the AI to detect whether your thumbs is in the up or down direction. Clicking the evaluate button, allows the AI to detect whether your thumbs is in the up direction or down direction, by turning on and updating the sliders.


