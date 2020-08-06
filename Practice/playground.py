
	

"""
Title: main.py
Author: Kristopher Ward
Group: IMMERSE  demos

    This file contains the class code for the Computer Vision Playground application
    This file also contains the main code to be ran when operating the application

"""
"""
########################################################################################################################
###   LIBRARIES   ###   LIBRARIES   ###   LIBRARIES   ###   LIBRARIES   ###   LIBRARIES   ###   LIBRARIES   ###   LIBRAR
########################################################################################################################
"""
# gui
import attributes as at
import tkinter as tk
from tkinter import messagebox
# image conversion
from PIL import Image
from PIL import ImageTk
# image processing
import cv2
# export image via email
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
# general
import numpy as np
import threading
import time
import sys
import global_class

"""
########################################################################################################################
###   COMPUTER VISION PLAYGROUND CLASS   ###   COMPUTER VISION PLAYGROUND CLASS   ###   COMPUTER VISION PLAYGROUND CLASS
########################################################################################################################
"""

camera = global_class.camera

class ComputerVisionPlayground(tk.Grid):
    """
    This class contains everthing needed to operate the Computer Vision Playground
    """
    def __init__(self):
        """
        This function will create the tkinter window used to run the CVP. This application
        uses scale bars to altar different mask values for openCV
        """

        """Important Globals/Flags"""
        self.frame = None
        self._ = None
        self.thread = None
        self.stopEvent = None

        self.print_contour = True
        self.take_photo = False
        self.canny_edges = False

        self.normal_frame = None
        self.hsv_frame = None
        self.masked_frame = None
        self.masked_hsv_frame = None

        self.send_frame_clr = None
        self.send_frame_hsv = None
        self.send_frame_msk = None
        self.send_frame_inv = None
        self.send_total = None

        """Video Source Initialization"""
        self.vs = camera#cv2.VideoCapture(0)
        if (not self.vs.isOpened()):
              self.vs = cv2.VideoCapture(at.VIDEO_SOURCE)
        # frame dimensions
        self.width = self.vs.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vs.get(cv2.CAP_PROP_FRAME_HEIGHT)
        # desired widths for the video source
        self.width = int(self.width / 2)
        self.height = int(self.height / 2)
        # let camera warm up
        time.sleep(at.CAMERA_INIT)

        """"Tkinter root initialization"""
        self.master = tk.Tk()
        # create a closing protocol
        self.master.wm_protocol("WM_DELETE_WINDOW", self.on_closing)
        self.master.attributes("-fullscreen", True)
        # zoom in on window created
        self.master.state("normal")
        # give our window a name
        self.master.wm_title(at.APP_TITLE)
        # color our background
        self.master.configure(background=at.APP_BG)
        # configure window size
        self.configure_window(self.master, at.APP_WIDTH, at.APP_HEIGHT, at.APP_CELL_SIZE_X, at.APP_CELL_SIZE_Y)

        # string variable to collect email used in image processing function
        self.email_address = tk.StringVar()

        """Menu Bar"""
        # create menu object
        self.menu_bar = tk.Menu(self.master)
        # configure it to current window
        self.master.configure(menu=self.menu_bar)
        # create our file down submenu and add it to the menu bar
        self.submenu_file = tk.Menu(self.menu_bar,
                                    tearoff=False)
        # let it cascade
        self.menu_bar.add_cascade(label="File",
                                  menu=self.submenu_file)
        # add separator
        self.submenu_file.add_separator()
        # add exit button
        self.submenu_file.add_command(label="Exit",
                                      command=self.on_closing)
        # create functions submenu
        self.submenu_functions = tk.Menu(self.menu_bar,
                                         tearoff=False)
        # add it to the menu bar
        self.menu_bar.add_cascade(label="Functions",
                                  menu=self.submenu_functions)
        self.submenu_functions.add_command(label="Take Photo",
                                           command=self.take_photo_button)
        self.submenu_functions.add_separator()
        # create a toggle contour button
        self.submenu_functions.add_command(label="Toggle Contour",
                                           command=self.toggle_contour)
        # toggle canny edges
        self.submenu_functions.add_command(label="Toggle Canny Edges",
                                           command=self.toggle_canny)
        # create a reset color button
        self.submenu_functions.add_command(label="Reset Colors",
                                           command=self.update_color_reset)

        """App Title Bar"""
        # create title label object
        self.title = tk.Label(self.master,
                              text=at.TITLE_TEXT,
                              font=at.TITLE_FONT,
                              bg=at.TITLE_BG,
                              fg=at.TITLE_FG,
                              relief=at.TITLE_RELIEF,
                              anchor=at.TITLE_ANCHOR)
        self.title.grid(row=at.TITLE_ROW,
                        column=at.TITLE_COLUMN,
                        rowspan=at.TITLE_ROWSPAN,
                        columnspan=at.TITLE_COLUMNSPAN,
                        sticky=at.TITLE_STICKY)

        """App Footnote"""
        self.footnote = tk.Label(self.master,
                                 text=at.FOOTNOTE_TEXT,
                                 font=at.FOOTNOTE_FONT,
                                 bg=at.FOOTNOTE_BG,
                                 fg=at.FOOTNOTE_FG,
                                 relief=at.FOOTNOTE_RELIEF,
                                 anchor=at.FOOTNOTE_ANCHOR)
        self.footnote.grid(row=at.FOOTNOTE_ROW,
                           column=at.FOOTNOTE_COLUMN,
                           rowspan=at.FOOTNOTE_ROWSPAN,
                           columnspan=at.FOOTNOTE_COLUMNSPAN,
                           sticky=at.FOOTNOTE_STICKY)

        """Lower Bound Color Range Widgets"""
        # these include headers, text and scale bar widgets
        # create a header
        self.lbc_header = tk.Label(self.master,
                                   text="\nLower Bound Colors",
                                   font=at.HEADER_FONT,
                                   bg=at.HEADER_BG,
                                   fg=at.HEADER_FG,
                                   relief=at.HEADER_RELIEF,
                                   anchor=at.HEADER_ANCHOR,)
        self.lbc_header.grid(row=at.HEADER_LBC_ROW,
                             column=at.HEADER_LBC_COLUMN,
                             rowspan=at.HEADER_ROWSPAN,
                             columnspan=at.HEADER_COLUMNSPAN,
                             sticky=at.HEADER_STICKY)
        # hue label
        self.lbc_hue_label = tk.Label(self.master,
                                      text="Hue:",
                                      font=at.TEXT_FONT,
                                      bg=at.TEXT_BG,
                                      fg=at.TEXT_FG,
                                      relief=at.TEXT_RELIEF,
                                      anchor=at.TEXT_ANCHOR,
                                      justify=at.TEXT_JUSTIFY)
        self.lbc_hue_label.grid(row=at.HEADER_LBC_ROW + 1,
                                column=at.HEADER_LBC_COLUMN,
                                rowspan=at.TEXT_ROWSPAN,
                                columnspan=at.TEXT_COLUMNSPAN,
                                sticky=at.TEXT_STICKY)
        # hue scale bar
        self.lbc_hue_scale = tk.Scale(self.master,
                                      from_=0,
                                      to=179,
                                      orient="horizontal",
                                      width=at.SCALE_WIDTH,
                                      length=at.SCALE_LENGTH,
                                      tickinterval=at.SCALE_TICKVALUE,
                                      bg=at.SCALE_BG,
                                      fg=at.SCALE_FG)
        self.lbc_hue_scale.grid(row=at.HEADER_LBC_ROW + 2,
                                column=at.HEADER_LBC_COLUMN,
                                rowspan=at.SCALE_ROWSPAN,
                                columnspan=at.SCALE_COLUMNSPAN,
                                sticky=at.SCALE_STICKY)
        # saturation label
        self.lbc_saturation_label = tk.Label(self.master,
                                             text="Saturation:",
                                             font=at.TEXT_FONT,
                                             bg=at.TEXT_BG,
                                             fg=at.TEXT_FG,
                                             relief=at.TEXT_RELIEF,
                                             anchor=at.TEXT_ANCHOR,
                                             justify=at.TEXT_JUSTIFY)
        self.lbc_saturation_label.grid(row=at.HEADER_LBC_ROW + 3,
                                       column=at.HEADER_LBC_COLUMN,
                                       rowspan=at.TEXT_ROWSPAN,
                                       columnspan=at.TEXT_COLUMNSPAN,
                                       sticky=at.TEXT_STICKY)
        # saturation scale bar
        self.lbc_saturation_scale = tk.Scale(self.master,
                                             from_=0,
                                             to=255,
                                             orient="horizontal",
                                             width=at.SCALE_WIDTH,
                                             length=at.SCALE_LENGTH,
                                             tickinterval=at.SCALE_TICKVALUE,
                                             bg=at.SCALE_BG,
                                             fg=at.SCALE_FG)
        self.lbc_saturation_scale.grid(row=at.HEADER_LBC_ROW + 4,
                                       column=at.HEADER_LBC_COLUMN,
                                       rowspan=at.SCALE_ROWSPAN,
                                       columnspan=at.SCALE_COLUMNSPAN,
                                       sticky=at.SCALE_STICKY)
        # Value label
        self.lbc_saturation_label = tk.Label(self.master,
                                             text="Brightness:",
                                             font=at.TEXT_FONT,
                                             bg=at.TEXT_BG,
                                             fg=at.TEXT_FG,
                                             relief=at.TEXT_RELIEF,
                                             anchor=at.TEXT_ANCHOR,
                                             justify=at.TEXT_JUSTIFY)
        self.lbc_saturation_label.grid(row=at.HEADER_LBC_ROW + 5,
                                       column=at.HEADER_LBC_COLUMN,
                                       rowspan=at.TEXT_ROWSPAN,
                                       columnspan=at.TEXT_COLUMNSPAN,
                                       sticky=at.TEXT_STICKY)
        self.lbc_value_scale = tk.Scale(self.master,
                                        from_=0,
                                        to=255,
                                        orient="horizontal",
                                        width=at.SCALE_WIDTH,
                                        length=at.SCALE_LENGTH,
                                        tickinterval=at.SCALE_TICKVALUE,
                                        bg=at.SCALE_BG,
                                        fg=at.SCALE_FG)
        self.lbc_value_scale.grid(row=at.HEADER_LBC_ROW + 6,
                                  column=at.HEADER_LBC_COLUMN,
                                  rowspan=at.SCALE_ROWSPAN,
                                  columnspan=at.SCALE_COLUMNSPAN,
                                  sticky=at.SCALE_STICKY)

        """Upper Bound Color Range Widgets"""
        # create a header
        self.ubc_header = tk.Label(self.master,
                                   text="\nUpper Bound Colors",
                                   font=at.HEADER_FONT,
                                   bg=at.HEADER_BG,
                                   fg=at.HEADER_FG,
                                   relief=at.HEADER_RELIEF,
                                   anchor=at.HEADER_ANCHOR,)
        self.ubc_header.grid(row=at.HEADER_UBC_ROW,
                             column=at.HEADER_UBC_COLUMN,
                             rowspan=at.HEADER_ROWSPAN,
                             columnspan=at.HEADER_COLUMNSPAN,
                             sticky=at.HEADER_STICKY)
        # hue label
        self.ubc_hue_label = tk.Label(self.master,
                                      text="Hue:",
                                      font=at.TEXT_FONT,
                                      bg=at.TEXT_BG,
                                      fg=at.TEXT_FG,
                                      relief=at.TEXT_RELIEF,
                                      anchor=at.TEXT_ANCHOR,
                                      justify=at.TEXT_JUSTIFY)
        self.ubc_hue_label.grid(row=at.HEADER_UBC_ROW + 1,
                                column=at.HEADER_UBC_COLUMN,
                                rowspan=at.TEXT_ROWSPAN,
                                columnspan=at.TEXT_COLUMNSPAN,
                                sticky=at.TEXT_STICKY)
        # hue scale bar
        self.ubc_hue_scale = tk.Scale(self.master,
                                      from_=0,
                                      to=179,
                                      orient="horizontal",
                                      width=at.SCALE_WIDTH,
                                      length=at.SCALE_LENGTH,
                                      tickinterval=at.SCALE_TICKVALUE,
                                      bg=at.SCALE_BG,
                                      fg=at.SCALE_FG)
        self.ubc_hue_scale.grid(row=at.HEADER_UBC_ROW + 2,
                                column=at.HEADER_UBC_COLUMN,
                                rowspan=at.SCALE_ROWSPAN,
                                columnspan=at.SCALE_COLUMNSPAN,
                                sticky=at.SCALE_STICKY)
        # saturation label
        self.ubc_saturation_label = tk.Label(self.master,
                                             text="Saturation:",
                                             font=at.TEXT_FONT,
                                             bg=at.TEXT_BG,
                                             fg=at.TEXT_FG,
                                             relief=at.TEXT_RELIEF,
                                             anchor=at.TEXT_ANCHOR,
                                             justify=at.TEXT_JUSTIFY)
        self.ubc_saturation_label.grid(row=at.HEADER_UBC_ROW + 3,
                                       column=at.HEADER_UBC_COLUMN,
                                       rowspan=at.TEXT_ROWSPAN,
                                       columnspan=at.TEXT_COLUMNSPAN,
                                       sticky=at.TEXT_STICKY)
        # saturation scale bar
        self.ubc_saturation_scale = tk.Scale(self.master,
                                             from_=0,
                                             to=255,
                                             orient="horizontal",
                                             width=at.SCALE_WIDTH,
                                             length=at.SCALE_LENGTH,
                                             tickinterval=at.SCALE_TICKVALUE,
                                             bg=at.SCALE_BG,
                                             fg=at.SCALE_FG)
        self.ubc_saturation_scale.grid(row=at.HEADER_UBC_ROW + 4,
                                       column=at.HEADER_UBC_COLUMN,
                                       rowspan=at.SCALE_ROWSPAN,
                                       columnspan=at.SCALE_COLUMNSPAN,
                                       sticky=at.SCALE_STICKY)
        # value label
        self.ubc_saturation_label = tk.Label(self.master,
                                             text="Brightness:",
                                             font=at.TEXT_FONT,
                                             bg=at.TEXT_BG,
                                             fg=at.TEXT_FG,
                                             relief=at.TEXT_RELIEF,
                                             anchor=at.TEXT_ANCHOR,
                                             justify=at.TEXT_JUSTIFY)
        self.ubc_saturation_label.grid(row=at.HEADER_UBC_ROW + 5,
                                       column=at.HEADER_UBC_COLUMN,
                                       rowspan=at.TEXT_ROWSPAN,
                                       columnspan=at.TEXT_COLUMNSPAN,
                                       sticky=at.TEXT_STICKY)
        # value scale bar
        self.ubc_value_scale = tk.Scale(self.master,
                                        from_=0,
                                        to=255,
                                        orient="horizontal",
                                        width=at.SCALE_WIDTH,
                                        length=at.SCALE_LENGTH,
                                        tickinterval=at.SCALE_TICKVALUE,
                                        bg=at.SCALE_BG,
                                        fg=at.SCALE_FG)
        self.ubc_value_scale.grid(row=at.HEADER_UBC_ROW + 6,
                                  column=at.HEADER_UBC_COLUMN,
                                  rowspan=at.SCALE_ROWSPAN,
                                  columnspan=at.SCALE_COLUMNSPAN,
                                  sticky=at.SCALE_STICKY)

        """Set default Scale Bar settings"""
        self.update_color_reset()

        """Color Preset Buttons"""
        # pressing this will change settings to look for yellow
        self.button_yellow = tk.Button(self.master,
                                       bg="#FFFF00",
                                       fg="#FFFF00",
                                       width=2,
                                       height=1,
                                       command=self.update_color_yellow)
        self.button_yellow.grid(row=at.APP_HEIGHT - 7,
                                column=1)

        # pressing this will change settings to look for green
        self.button_green = tk.Button(self.master,
                                      bg="#00FF00",
                                      fg="#00FF00",
                                      width=at.BUTTON_WIDTH,
                                      height=at.BUTTON_HEIGHT,
                                      command=self.update_color_green)
        self.button_green.grid(row=at.APP_HEIGHT - 6,
                               column=1)

        # pressing this will change settings to look for cyan
        self.button_cyan = tk.Button(self.master,
                                     bg="#00FFFF",
                                     fg="#00FFFF",
                                     width=at.BUTTON_WIDTH,
                                     height=at.BUTTON_HEIGHT,
                                     command=self.update_color_cyan)
        self.button_cyan.grid(row=at.APP_HEIGHT - 5,
                              column=1)

        # pressing this will change settings to look for orange
        self.button_orange = tk.Button(self.master,
                                       bg="#ff7f00",
                                       fg="#ff7f00",
                                       width=at.BUTTON_WIDTH,
                                       height=at.BUTTON_HEIGHT,
                                       command=self.update_color_orange)
        self.button_orange.grid(row=at.APP_HEIGHT - 4,
                                column=1)

        # pressing this will change settings to look for magenta
        self.button_magenta = tk.Button(self.master,
                                        bg="#FF00FF",
                                        fg="#FF00FF",
                                        width=at.BUTTON_WIDTH,
                                        height=at.BUTTON_HEIGHT,
                                        command=self.update_color_magenta)
        self.button_magenta.grid(row=at.APP_HEIGHT - 3,
                                 column=1)

        """Video Feed Labels"""
        # create a header_normal
        self.header_normal = tk.Label(self.master,
                                      text="\nNormal Feed",
                                      font=at.HEADER_FONT,
                                      bg=at.HEADER_BG,
                                      fg=at.HEADER_FG,
                                      relief=at.HEADER_RELIEF,
                                      anchor=at.HEADER_ANCHOR,)
        self.header_normal.grid(row=at.HEADER_N_FEED_ROW,
                                column=at.HEADER_N_FEED_COLUMN,
                                rowspan=at.HEADER_ROWSPAN,
                                columnspan=at.HEADER_COLUMNSPAN,
                                sticky=at.HEADER_STICKY)

        # create a header_hsv
        self.header_hsv = tk.Label(self.master,
                                   text="\nHSV Feed",
                                   font=at.HEADER_FONT,
                                   bg=at.HEADER_BG,
                                   fg=at.HEADER_FG,
                                   relief=at.HEADER_RELIEF,
                                   anchor=at.HEADER_ANCHOR,)
        self.header_hsv.grid(row=at.HEADER_HSV_FEED_ROW,
                             column=at.HEADER_HSV_FEED_COLUMN,
                             rowspan=at.HEADER_ROWSPAN,
                             columnspan=at.HEADER_COLUMNSPAN,
                             sticky=at.HEADER_STICKY)

        # create a header_masked
        self.header_masked = tk.Label(self.master,
                                      text="\nMasked Inverted Feed",
                                      font=at.HEADER_FONT,
                                      bg=at.HEADER_BG,
                                      fg=at.HEADER_FG,
                                      relief=at.HEADER_RELIEF,
                                      anchor=at.HEADER_ANCHOR,)
        self.header_masked.grid(row=at.HEADER_M_FEED_ROW,
                                column=at.HEADER_M_FEED_COLUMN,
                                rowspan=at.HEADER_ROWSPAN,
                                columnspan=at.HEADER_COLUMNSPAN,
                                sticky=at.HEADER_STICKY)

        # create a header_inverted
        self.header_masked_clr = tk.Label(self.master,
                                          text="\nMasked Color Feed",
                                          font=at.HEADER_FONT,
                                          bg=at.HEADER_BG,
                                          fg=at.HEADER_FG,
                                          relief=at.HEADER_RELIEF,
                                          anchor=at.HEADER_ANCHOR,)
        self.header_masked_clr.grid(row=at.HEADER_I_FEED_ROW,
                                    column=at.HEADER_I_FEED_COLUMN,
                                    rowspan=at.HEADER_ROWSPAN,
                                    columnspan=at.HEADER_COLUMNSPAN,
                                    sticky=at.HEADER_STICKY)

        """"HSV Spectrum Picture"""
        self.header_inverted = tk.Label(self.master,
                                        text="\nHSV Spectrum",
                                        font=at.HEADER_FONT,
                                        bg=at.HEADER_BG,
                                        fg=at.HEADER_FG,
                                        relief=at.HEADER_RELIEF,
                                        anchor=at.HEADER_ANCHOR,)
        self.header_inverted.grid(row=at.HEADER_HSV_ROW,
                                  column=at.HEADER_HSV_COLUMN,
                                  rowspan=at.HEADER_ROWSPAN,
                                  columnspan=at.HEADER_COLUMNSPAN,
                                  sticky=at.HEADER_STICKY)
        # place hsv image
        self.photo = Image.open("hsv_scale.jpg")
        # pull picture dimensions
        self.im_width, self.im_height = self.photo.size
        # do some math to resize photo to be same height as video feed
        self.photo = self.photo.resize(((int(self.im_width*self.height / self.im_height)), int(self.height)))
        # convert photo to tk Format
        self.photo = ImageTk.PhotoImage(self.photo)
        # create a label widget to place it in
        self.photo_label = tk.Label(self.master,
                                    image=self.photo)
        # save as new photo
        self.photo_label.photo = self.photo
        # place photo in window
        self.photo_label.grid(row=at.HEADER_HSV_ROW + 1,
                              column=at.HEADER_HSV_COLUMN + 1,
                              rowspan=at.IMAGE_ROWSPAN,
                              columnspan=at.IMAGE_COLUMNSPAN_LONG,
                              sticky=at.IMAGE_STICKY_PHOTO)

        """Image Processing Thread"""
        # stop event is used to leave image processing loop if something happens to the camera
        self.stopEvent = threading.Event()
        # create thread with image processing as its target
        self.thread = threading.Thread(target=self.image_processing)
        # when set to true, this thread will die if main thread dies
        self.thread.daemon = True
        # begin thread
        self.thread.start()

    def take_photo_button(self):
        """
        will start countdown in new thread
        """
        countdown_thread = threading.Thread(target=self.start_countdown)
        countdown_thread.daemon = True
        countdown_thread.start()

    def start_countdown(self):
        """
        This function is meant to be ran in a thread separate to the main thread
        This will flash colors on the screen to indicate a camera
        """
        # grab countdown its about 5 seconds
        count = at.CD_COUNT
        # toggle colors on screen
        for i in range(count - 1):
            self.title.configure(bg=at.FOOTNOTE_BG)
            time.sleep(0.5)
            self.title.configure(bg=at.TITLE_BG)
            time.sleep(0.5)
        # toggle faster
        for i in range(10):
            self.title.configure(bg=at.FOOTNOTE_BG)
            time.sleep(0.05)
            self.title.configure(bg=at.TITLE_BG)
            time.sleep(0.05)
        # raise flag
        self.take_photo = True

    def image_processing(self):
        """
        This function is ran on a background thread. This function will
        read data from the camera and process it through the python openCV
        library
        """
        # create try loop to try to begin capturing video
        try:
            while not self.stopEvent.is_set():
                # get scale information
                # get scale bar values
                l_h = self.lbc_hue_scale.get()
                l_s = self.lbc_saturation_scale.get()
                l_v = self.lbc_value_scale.get()
                u_h = self.ubc_hue_scale.get()
                u_s = self.ubc_saturation_scale.get()
                u_v = self.ubc_value_scale.get()

                # create lower and upper bound tuples for cv2 range function
                lower_bound = np.array([l_h, l_s, l_v])
                upper_bound = np.array([u_h, u_s, u_v])

                # grab frame, "_" is just a throw away thats needed to get the tuple that
                # vs.read will return
                self._, self.frame = self.vs.read()
                # resize frame to half size
                self.frame = cv2.resize(self.frame, None, fx=0.5, fy=0.5)
                # get color frame
                org_frame_clr = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                # get hsv frame
                org_frame_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
                # get mask
                org_frame_msk = cv2.inRange(org_frame_hsv, lower_bound, upper_bound)
                # get inverted
                org_frame_msk_hsv = cv2.bitwise_and(org_frame_clr, org_frame_clr, mask=org_frame_msk)

                # canny edges
                org_canny_edges = cv2.Canny(self.frame, 100, 200)

                if self.print_contour:
                    # erode and dilate mask to find better contours
                    org_frame_msk = cv2.erode(org_frame_msk, None, iterations=2)
                    org_frame_msk = cv2.dilate(org_frame_msk, None, iterations=2)

                if self.print_contour:
                    # get contours
                    contours, _ = cv2.findContours(org_frame_msk, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
                    # draw contours - param(frame, contours, draw_state, color, thickness
                    cv2.drawContours(org_frame_clr, contours, 0, (255, 0, 144), 2)
                    cv2.drawContours(org_frame_hsv, contours, 0, (255, 0, 144), 2)
                    cv2.drawContours(org_frame_msk_hsv, contours, 0, (255, 0, 144), 2)

                # convert images to PIL format
                org_frame_clr = Image.fromarray(org_frame_clr)
                org_frame_hsv = Image.fromarray(org_frame_hsv)
                org_frame_msk = Image.fromarray(org_frame_msk)
                org_frame_msk_hsv = Image.fromarray(org_frame_msk_hsv)
                org_canny_edges = Image.fromarray(org_canny_edges)


                # convert to Tk format
                frame_clr = ImageTk.PhotoImage(org_frame_clr)
                frame_hsv = ImageTk.PhotoImage(org_frame_hsv)
                frame_msk = ImageTk.PhotoImage(org_frame_msk)
                frame_msk_hsv = ImageTk.PhotoImage(org_frame_msk_hsv)
                frame_canny = ImageTk.PhotoImage(org_canny_edges)

                # if the normal frame is beginning
                if self.normal_frame is None:
                    # create a label for the image to be placed in
                    self.normal_frame = tk.Label(image=frame_clr)
                    # save image
                    self.normal_frame.image = frame_clr
                    # place image
                    self.normal_frame.grid(row=at.HEADER_N_FEED_ROW + 1,
                                           column=at.HEADER_N_FEED_COLUMN,
                                           rowspan=at.IMAGE_ROWSPAN,
                                           columnspan=at.IMAGE_COLUMNSPAN,
                                           sticky=at.IMAGE_STICKY)
                # update image with new frame
                else:
                    # update image
                    self.normal_frame.configure(image=frame_clr)
                    # save image
                    self.normal_frame.image = frame_clr

                # if the hsv frame is beginning
                if self.hsv_frame is None:
                    # create a label for the image to be placed in
                    self.hsv_frame = tk.Label(image=frame_hsv)
                    # save image
                    self.hsv_frame.image = frame_hsv
                    # place image
                    self.hsv_frame.grid(row=at.HEADER_HSV_FEED_ROW + 1,
                                        column=at.HEADER_HSV_FEED_COLUMN,
                                        rowspan=at.IMAGE_ROWSPAN,
                                        columnspan=at.IMAGE_COLUMNSPAN,
                                        sticky=at.IMAGE_STICKY)
                # update image with new frame
                else:
                    # update image
                    self.hsv_frame.configure(image=frame_hsv)
                    # save frame
                    self.hsv_frame.image = frame_hsv

                # if the masked frame is beginning
                if self.masked_frame is None:
                    # create a label for the image to be placed in
                    self.masked_frame = tk.Label(image=frame_msk)
                    # save image
                    self.masked_frame.image = frame_msk
                    # place image
                    self.masked_frame.grid(row=at.HEADER_M_FEED_ROW + 1,
                                           column=at.HEADER_M_FEED_COLUMN,
                                           rowspan=at.IMAGE_ROWSPAN,
                                           columnspan=at.IMAGE_COLUMNSPAN,
                                           sticky=at.IMAGE_STICKY)
                # update image with new frame
                else:
                    # update image
                    self.masked_frame.configure(image=frame_msk)
                    # save image
                    self.masked_frame.image = frame_msk

                # if the masked hsv frame is beginning
                if self.masked_hsv_frame is None:
                    # create a label for the image to be placed in
                    self.masked_hsv_frame = tk.Label(image=frame_msk_hsv)
                    # save image
                    self.masked_hsv_frame.image = frame_msk_hsv
                    # place image
                    self.masked_hsv_frame.grid(row=at.HEADER_I_FEED_ROW + 1,
                                               column=at.HEADER_I_FEED_COLUMN,
                                               rowspan=at.IMAGE_ROWSPAN,
                                               columnspan=at.IMAGE_COLUMNSPAN,
                                               sticky=at.IMAGE_STICKY)
                # update image with new frame
                else:
                    if self.canny_edges:
                        # update image
                        self.masked_hsv_frame.configure(image=frame_canny)
                        # save image
                        self.masked_hsv_frame.image = frame_canny
                    else:
                        # update image
                        self.masked_hsv_frame.configure(image=frame_msk_hsv)
                        # save image
                        self.masked_hsv_frame.image = frame_msk_hsv

                # if take photo is in effect
                if self.take_photo:
                    # lower flag
                    self.take_photo = False
                    # clear entry box
                    self.email_address.set("")
                    # create top level gui
                    take_photo_window = tk.Toplevel()
                    # configure window
                    self.configure_window(take_photo_window, 10, 12, 10, 10)
                    # # put away the home screen temporarily
                    # self.master.withdraw()
                    # name window
                    take_photo_window.wm_title("Photo Booth")
                    # save frames for this window only
                    self.send_frame_clr = org_frame_clr
                    self.send_frame_hsv = org_frame_hsv
                    self.send_frame_msk = org_frame_msk
                    if self.canny_edges:
                        self.send_frame_msk_hsv = org_canny_edges
                    else:
                        self.send_frame_msk_hsv = org_frame_msk_hsv
                    # save current tk frames to display
                    this_frame_clr = frame_clr
                    this_frame_hsv = frame_hsv
                    this_frame_msk = frame_msk
                    if self.canny_edges:
                        this_frame_msk_hsv = frame_canny
                    else:
                        this_frame_msk_hsv = frame_msk_hsv
                    # insert the 4 different current frames into the window
                    normal_pic = tk.Label(take_photo_window,
                                          anchor="se",
                                          padx=0,
                                          pady=0,
                                          image=this_frame_clr)
                    normal_pic.grid(row=0,
                                    column=0,
                                    rowspan=5,
                                    columnspan=5,
                                    sticky="nsew")
                    hsv_pic = tk.Label(take_photo_window,
                                       anchor="sw",
                                       padx=0,
                                       pady=0,
                                       image=this_frame_hsv)
                    hsv_pic.grid(row=5,
                                 column=5,
                                 rowspan=5,
                                 columnspan=5,
                                 sticky="nsew")
                    masked_pic = tk.Label(take_photo_window,
                                          anchor="ne",
                                          padx=0,
                                          pady=0,
                                          image=this_frame_msk)
                    masked_pic.grid(row=5,
                                    column=0,
                                    rowspan=5,
                                    columnspan=5,
                                    sticky="nsew")
                    inverted_pic = tk.Label(take_photo_window,
                                            anchor="nw",
                                            padx=0,
                                            pady=0,
                                            image=this_frame_msk_hsv)
                    inverted_pic.grid(row=0,
                                      column=5,
                                      rowspan=5,
                                      columnspan=5,
                                      sticky="nsew")
                    # add email information
                    email_label = tk.Label(take_photo_window,
                                           text="email: ",
                                           font=at.TEXT_FONT,
                                           anchor="e")
                    email_label.grid(row=10,
                                     column=0,
                                     rowspan=2,
                                     columnspan=2,
                                     sticky="nsew")
                    # add email entry field
                    email_entry = tk.Entry(take_photo_window,
                                           textvariable=self.email_address,
                                           font=at.TEXT_FONT)
                    email_entry.grid(row=10,
                                     column=2,
                                     rowspan=2,
                                     columnspan=6,
                                     sticky="nsew")
                    # send email button
                    send_button = tk.Button(take_photo_window,
                                            text="SEND",
                                            font=at.HEADER_FONT,
                                            bg=at.COLOR_2,
                                            fg=at.COLOR_1,
                                            relief="raised",
                                            command=self.email_photos)
                    send_button.grid(row=10,
                                     column=8,
                                     rowspan=2,
                                     columnspan=2,
                                     sticky="nsew")
                    # create new image
                    self.send_total = Image.new(mode="RGB",
                                                size=(2 * self.width + 7, 2 * self.height + 7),
                                                color="white")
                    # paste current images to new image
                    self.send_total.paste(self.send_frame_clr, (3, 3))
                    self.send_total.paste(self.send_frame_hsv, (self.width + 4, self.height + 4))
                    self.send_total.paste(self.send_frame_msk, (3, self.height + 4))
                    self.send_total.paste(self.send_frame_msk_hsv, (self.width + 4, 3))
                    # save image
                    self.send_total.save("Image.jpg")

        # runtime error if camera doesnt work
        except RuntimeError:
            pass

    def verify_email(self):
        """
        This function looks for @ and . to verify if its a true email address
        """
        contains_dot = False
        contains_ampersand = False
        for char in self.email_address.get():
            if char == '@':
                contains_ampersand = True
            if char == '.':
                contains_dot = True
        if contains_ampersand and contains_dot:
            return True
        else:
            tk.messagebox.showerror("Error",
                                    "Please enter a valid email Address")
            return False

    def email_photos(self):
        """
        This function will email photos out
        """
        # try block to try to send photos
        try:
            # verify email
            if self.verify_email():
                # save important email addresses
                from_address = "IMMERSEcvp@gmail.com"
                to_address = self.email_address.get()

                # create message blocks
                msg = MIMEMultipart()

                # store relative info into msg
                msg['From'] = from_address
                msg['To'] = to_address
                msg['Subject'] = "Computer Vision Playground Photo"
                # attach body of message
                body = "Enjoy the photo! - BYU Department of Electrical and Computer Engineering"
                msg.attach(MIMEText(body, 'plain'))

                filename = "Image.jpg"
                # open image
                image_data = open(filename, 'rb').read()
                # attach image
                image = MIMEImage(image_data, name=os.path.basename(filename))
                msg.attach(image)

                # create SMTP session (Server, Portnumber)
                session = smtplib.SMTP('smtp.gmail.com', 587)
                # start TLS for security
                session.starttls()
                # authentication
                session.login(from_address, "BrighamYoung1875")
                # convert multipart msg into a string
                text = msg.as_string()
                # send the mail
                session.sendmail(from_address, to_address, text)
                # terminate session
                session.quit()

                # send message indicating completion
                tk.messagebox.showinfo("Message Send",
                                       "Photo sent to \"" + to_address + "\"")
            else:
                return
        except:
            tk.messagebox.showerror("Error",
                                    "Could not send photo out")

    def on_closing(self):
        """
        called to close the application
        """
        # ask quit
        result = tk.messagebox.askquestion("Exit",
                                           "Do you wish to exit?")
        if result == "yes":
            # release camera
            self.vs.release()
            # destroy all camera windows
            cv2.destroyAllWindows()
            # try to erase Image.jpg
            try:
                os.remove("Image.jpg")
            except OSError:
                pass
            # exit system
            sys.exit()
        else:
            return

    def configure_window(self, master, width, height, cell_size_x, cell_size_y):
        """
         will configure any window passed into it and center it
        """
        # configure columns
        for i in range(width):
            master.columnconfigure(i,
                                   weight=1,
                                   minsize=cell_size_x)
        # configure rows
        for j in range(height - 1):
            master.rowconfigure(j,
                                weight=1,
                                minsize=cell_size_y)
        # center window now
        window_width = master.winfo_reqwidth()
        window_height = master.winfo_reqheight()
        # gets the coordinates of where the window needs to go
        position_right = int(master.winfo_screenwidth() / 2 - window_width / 2)
        position_down = int(master.winfo_screenheight() / 2 - window_height / 2)
        # position the window in the center of the page
        master.geometry("+{}+{}".format(position_right, position_down))

    def update_color_reset(self):
        """
        called to reset the scale bars to how they are on startup
        """
        self.lbc_hue_scale.set(0)
        self.lbc_saturation_scale.set(0)
        self.lbc_value_scale.set(120)
        self.ubc_hue_scale.set(179)
        self.ubc_saturation_scale.set(255)
        self.ubc_value_scale.set(255)

    def update_color_yellow(self):
        """
        called to move scale bars to yellow range
        """
        self.lbc_hue_scale.set(10)
        self.lbc_saturation_scale.set(100)
        self.lbc_value_scale.set(100)
        self.ubc_hue_scale.set(50)
        self.ubc_saturation_scale.set(170)
        self.ubc_value_scale.set(170)

    def update_color_green(self):
        """
        called to move scale bars to green range
        """
        self.lbc_hue_scale.set(30)
        self.lbc_saturation_scale.set(90)
        self.lbc_value_scale.set(0)
        self.ubc_hue_scale.set(90)
        self.ubc_saturation_scale.set(170)
        self.ubc_value_scale.set(80)

    def update_color_cyan(self):
        """
        called to move scale bars to cyan range
        """
        self.lbc_hue_scale.set(90)
        self.lbc_saturation_scale.set(225)
        self.lbc_value_scale.set(50)
        self.ubc_hue_scale.set(105)
        self.ubc_saturation_scale.set(255)
        self.ubc_value_scale.set(100)

    def update_color_orange(self):
        """
        called to move scale bars to orange range
        """
        self.lbc_hue_scale.set(0)
        self.lbc_saturation_scale.set(175)
        self.lbc_value_scale.set(70)
        self.ubc_hue_scale.set(20)
        self.ubc_saturation_scale.set(255)
        self.ubc_value_scale.set(120)

    def update_color_magenta(self):
        """
        called to move scale bars to magenta range
        """
        self.lbc_hue_scale.set(140)
        self.lbc_saturation_scale.set(105)
        self.lbc_value_scale.set(50)
        self.ubc_hue_scale.set(179)
        self.ubc_saturation_scale.set(255)
        self.ubc_value_scale.set(120)

    def toggle_contour(self):
        """
        Will toggle global variable associated with drawing contours
        """
        self.print_contour = not self.print_contour

    def toggle_canny(self):
        """
        Will toggle global variable associated with canny edges
        :return:
        """
        self.canny_edges = not self.canny_edges
        if self.canny_edges:
            self.header_masked_clr.configure(text="\nCanny Edges")
        else:
            self.header_masked_clr.configure(text="\nMasked Color Feed")


# will enter if statement only if this is the file being called from terminal
# if __name__ == "__main__":
#     # create our main window
#     mainApp = ComputerVisionPlayground()
#     # run our main loop
#     mainApp.master.mainloop()

