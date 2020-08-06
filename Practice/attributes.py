"""
Title: attributes.py
Author: Kristopher Ward
Group: IMMERSE demos

    This file contains attributes of the application that runs the Computer Vision Playground

"""

"""Camera"""
# 0 is the first camera attached to any device
VIDEO_SOURCE = 0
CAMERA_INIT = 2

"""Color Schemes"""
COLOR_1 = "#ffffff"  # app background
COLOR_2 = "#3a5998"  # title color
COLOR_3 = "#8b9dc3"  # footnote color
COLOR_4 = "#000000"  # text color
COLOR_5 = "#dfe3ee"  # misc

"""App Characteristics"""
APP_TITLE = "Computer Vision Playground"
APP_BG = COLOR_1
APP_WIDTH = 26
APP_HEIGHT = 17
APP_CELL_SIZE_X = 20
APP_CELL_SIZE_Y = 20
APP_FONT = "\"Yu Gothic\""


"""App Title Characteristics"""
TITLE_TEXT = "\n Computer Vision Playground"
TITLE_FONT = APP_FONT + " 24 bold"
TITLE_BG = COLOR_2
TITLE_FG = COLOR_1
TITLE_RELIEF = "flat"
TITLE_ANCHOR = "sw"

TITLE_ROW = 0
TITLE_COLUMN = 0
TITLE_ROWSPAN = 2
TITLE_COLUMNSPAN = APP_WIDTH
TITLE_STICKY = "nsew"

"""App Footnote Characteristics"""
FOOTNOTE_TEXT = "ECEn IMMERSE Demos"
FOOTNOTE_FONT = APP_FONT + " 10"
FOOTNOTE_BG = COLOR_3
FOOTNOTE_FG = COLOR_4
FOOTNOTE_RELIEF = "flat"
FOOTNOTE_ANCHOR = "se"

FOOTNOTE_ROW = APP_HEIGHT - 1
FOOTNOTE_COLUMN = 0
FOOTNOTE_ROWSPAN = 1
FOOTNOTE_COLUMNSPAN = APP_WIDTH
FOOTNOTE_STICKY = "nsew"

"""App Header Characteristics"""
HEADER_FONT = APP_FONT + " 12 bold"
HEADER_BG = COLOR_1
HEADER_FG = COLOR_2
HEADER_RELIEF = "flat"
HEADER_ANCHOR = "nw"

HEADER_ROWSPAN = 1
HEADER_COLUMNSPAN = 4
HEADER_STICKY = "nsew"

"""Header Anchors"""
HEADER_LBC_ROW = 2
HEADER_LBC_COLUMN = 2

HEADER_UBC_ROW = 2
HEADER_UBC_COLUMN = 8

HEADER_N_FEED_ROW = 2
HEADER_N_FEED_COLUMN = 14

HEADER_HSV_FEED_ROW = 9
HEADER_HSV_FEED_COLUMN = 20

HEADER_M_FEED_ROW = 9
HEADER_M_FEED_COLUMN = 14

HEADER_I_FEED_ROW = 2
HEADER_I_FEED_COLUMN = 20

HEADER_HSV_ROW = 9
HEADER_HSV_COLUMN = 1

"""Text Characteristics"""
TEXT_FONT = APP_FONT + " 10 bold"
TEXT_BG = COLOR_1
TEXT_FG = COLOR_4
TEXT_RELIEF = "flat"
TEXT_ANCHOR = "w"
TEXT_JUSTIFY = "left"

TEXT_ROWSPAN = 1
TEXT_COLUMNSPAN = 4
TEXT_STICKY = "nsew"

"""Scale Bar Characteristics"""
SCALE_BG = COLOR_1
SCALE_FG = COLOR_2

SCALE_ROWSPAN = 1
SCALE_COLUMNSPAN = 4
SCALE_STICKY = "ns"
SCALE_WIDTH = 20
SCALE_LENGTH = 200
SCALE_TICKVALUE = 50

"""Image Characteristics"""
IMAGE_ROWSPAN = 5
IMAGE_COLUMNSPAN = 5
IMAGE_COLUMNSPAN_LONG = 12
IMAGE_STICKY = "nsew"
IMAGE_RELIEF = "sunken"
IMAGE_BG = COLOR_3
IMAGE_STICKY_PHOTO = "w"

"""Button Characteristice"""
BUTTON_WIDTH = 2
BUTTON_HEIGHT = 1

"""Countdown Characteristics"""
CD_ROW = 8
CD_COLUMN = 19
CD_FONT = APP_FONT + " 12 bold"
CD_WIDTH = 1
CD_HEIGHT = 1
CD_BG = APP_BG
CD_FG = "red"
CD_COUNT = 5
