#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

import copy
import json
from pathlib import Path, PurePath
import os

# colors
color_list = [
    (  0,   0,   0, 255),  # black
    (255,   0,   0, 255),  # red
    (  0, 255,   0, 255),  # green
    (  0,   0, 255, 255),  # blue
    (128,   0, 128, 255),  # purple
    (255, 165,   0, 255),  # orange
    (255, 255,   0, 255),  # yellow
    (  0, 255, 255, 255),  # cyan
    (255,   0, 255, 255),  # fuchia
    (255, 192, 203, 255),  # pink
    ( 34, 139,  34, 255),  # forestgreen
    (211, 211, 211, 255),  # lightgray
    (160,  82,  45, 255),  # sienna
    (128, 128, 128, 255),  # gray
    ( 65, 105, 225, 255),  # royalblue
    (135, 206, 235, 255),  # skyblue
    (  0,   0, 139, 255),  # darkblue
    (255, 240, 240, 255),
    (135, 135, 135, 255),
    (135, 135, 135, 255),
    (135, 135, 135, 255),
    (135, 135, 135, 255),
    (135, 135, 135, 255),
    (135, 135, 135, 255),
    (135, 135, 135, 255),
    (135, 135, 135, 255),
    (135, 135, 135, 255),
    (135, 135, 135, 255),
    (135, 135, 135, 255),
    (135, 135, 135, 255),
    (135, 135, 135, 255),
    (135, 135, 135, 255),
    (135, 135, 135, 255)
    ]

# the path to the images
#print (os.path.basename(__file__))
png_path = os.path.dirname(__file__) + "/graphics/"
#print (png_path)


# the basic game unit for images and moving is
img_pix = 64


half_img_pix = img_pix//2


# animation pixels moved (it must be a factor of img_pix otherwise
#   the marble won't match with the grid of coordinates - i.e. there's
#   no wiggle room in the collision detection)...
tic_pix = img_pix // 2


#   save game location and initial file
# you can always save/load other names, 
# this is just a suggestion...
suggested_fn = "save.json"
this_fn_to_open = suggested_fn
this_fn_to_save = suggested_fn

home = Path.home()
saved_dir = None


# save file directory
if (os.name == "posix"):
    home = Path.home()
    data_path = home / Path(".local/share/npath")
else:
    print ("  Npath doesn't know where to set data_path for OS : ", os.name)
    print ("This is where a user would save their games.")


# configure location and file
config_filename = "config_npath.json"
if (os.name == "posix"):
    home = Path.home()
    config_path = home / Path(".config/npath")
    full_config_filename = config_path / config_filename
else:
    print ("  Npath doesn't know where to set config_path for OS : ", os.name)
    print ("This is where the game saves configuration parameters.")


# when loading a game from a file we put stuff in
# these spots so that DrawBoard can use them.
# changing dimensions in the config dialog also uses
# these.
new_game_cols = None
new_game_rows = None
new_borders = None
new_board = None


# which board to show, a toggle between 0, 1  when Key F2 is pressed
#    but we start at 2 for a new board and it's random to start...
# 0 - puzzle to solve
# 1 - guesses placed
# 2 - blank background
#
show_board = 2
do_random_board = True


# options which affect board layout and size below
# and also the display of some sprites
borders = True
if (borders == True):
    adj_size = 2
else:
    adj_size = 0

default_borders = True

# current, default and changed parameters

min_cols = 1     # must be 1 or greater
min_rows = 1     # 

max_cols = 50    # for temporary testing
max_rows = 50    #

#max_cols = 28     # on 1920 x 1080
#max_rows = 13     # on 1920 x 1080

game_cols = 2     # width
game_rows = 2     # height

default_game_cols = 4     # width
default_game_rows = 4     # height


# need to keep track of the current square
square = None

# if the user has to wait until something 
#  (usually the animation) is done
no_user_actions = False

