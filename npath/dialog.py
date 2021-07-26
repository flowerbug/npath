#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

import os
import pyglet
import sys
import copy
import json
from pathlib import Path

import config as cfg

from board import ClearBoard, ResizeBoard
from version import GetVersion


# print configuration parameters
def print_cfg ():
    print ("Config Values")
    print ("Current    Borders : %-5s" %cfg.borders, "  Rows, Cols : ", cfg.game_rows, cfg.game_cols)
    print ("New        Borders : %-5s" %cfg.new_borders, "  Rows, Cols : ", cfg.new_game_rows, cfg.new_game_cols)
    print ("Defaults   Borders : %-5s" %cfg.default_borders, "  Rows, Cols : ", cfg.default_game_rows, cfg.default_game_cols)


# not sure I'm keeping this yet...
def RestoreConfigDefaults():
    print ("Restore Config Defaults")
    cfg.game_rows = cfg.default_game_rows
    cfg.game_cols = cfg.default_game_cols
    cfg.borders = cfg.default_borders
    if (cfg.show_board != 2):
        print("Npath configuration parameters reset now using default values")


def ShowAbout (self):
    print(
        "\n    Npath is running in directory : " + str(Path.cwd()) + "\n"
        "    Npath code is running from directory : " + os.path.dirname(__file__) + "\n"
        + "\n"
        + "      It saves game files to directory : " + str(cfg.data_path) + "\n"
        + "\n"
        "    Npath Version is : " + GetVersion() + "\n"
        + "\n"
        + "        Open file name : " + str(cfg.this_fn_to_open) + "\n"
        + "        Save file name : " + str(cfg.this_fn_to_save) + "\n"
        + "\n"
        + "\n"
        + "      It keeps the configuration settings with the saved game.\n"
        + "\n")
    print_cfg()
    print(
        "\n\n"
        + "    'ESC' or 'Q'        : Quit\n"
        + "                             Quitting DOES NOT save the Game\n"
        + "\n"
        + "    'F1', 'H', or '?'   : Help (this screen)\n"
        + "\n"
        + "    'F2'                : Show or Hide guesses\n"
        + "                             Only the 'Q', 'ESC', 'F1', 'H', or '?' keys will work when showing guesses\n"
        + "\n"
        + "    'F3'                : Toggle Border\n"
        + "\n"
        + "\n"
        + "    'Arrow Keys'        : Increase or Decrease Columns and Rows\n"
        + "\n"
        + "\n"
        + "    'F6'                : Load Game From File\n"
        + "    'F7'                : Save Game To File\n"
        + "\n"
        + "    'F8'                : New Random Game\n"
        + "    'F9'                : Restart Current Game\n"
        + "\n"
        + "    'F10'               : Check Game\n"
        + "                             To see if we've won\n"
        + "\n"
        + "\n"
        + "    'F11'               : Delete Saved Game and Directory\n"
        + "\n"
        + "\n"
        + "    Project Location :"
        + "    https://www.github.com/flowerbug/npath\n"
        + "\n"
        )


def ChangeLayout(self):
    print ("ChangeLayout")
    cfg.borders = not cfg.borders
    if (cfg.borders == True):
        cfg.adj_size = 2
    else:
        cfg.adj_size = 0
    ResizeBoard (self)
    cfg.show_board = 2  # reinitialize sprites and lists


def Load_NPATHSave_Version_1 (self, lines_in):

    cfg.new_borders = lines_in[1][0]
    cfg.new_game_rows = lines_in[1][1]
    cfg.new_game_cols = lines_in[1][2]

    cfg.new_board = []
    cfg.new_board = copy.deepcopy(lines_in[2])

    # we're going to have to redraw the board
    # but we aren't a random board
    cfg.show_board = 2
    cfg.do_random_board = False

    print ("Load_NPATHSave_Version_1 -> new variables NewBorders NR NC NewBoard", cfg.new_borders, cfg.new_game_rows, cfg.new_game_cols, cfg.new_board)


def LoadGame (self):
    print ("Load Game")
    cfg.saved_dir = str(Path.cwd())
    print ("Keep track of current directory : ", cfg.saved_dir)

    # check for saved games directory
    if (cfg.data_path.exists() != True):
        print("Npath Save Game Directory Missing.  You haven't created : " + str(cfg.data_path) + " yet")
        return

    # is there anything in there?
    if (len(os.listdir(path=str(cfg.data_path))) == 0):
        print("Npath Save Game Directory Is Empty.")
        return

    print ("Changing directory to : ", str(cfg.data_path))
    os.chdir(str(cfg.data_path))

    if (cfg.this_fn_to_open == None):
        print ("LoadGame...  No file selected...")
        os.chdir(cfg.saved_dir)
        return

    if (cfg.this_fn_to_open.endswith(".json") == True):
        with open(cfg.this_fn_to_open) as filein:
            lines_in = json.load(filein)
        print ("fn : ", cfg.this_fn_to_open, " lines in : ", lines_in)
        Load_NPATHSave_Version_1 (self, lines_in)
        cfg.show_board = 2  # reinitialize sprites and lists
        cfg.do_random_board = False
        cfg.this_fn_to_save = cfg.this_fn_to_open

    #print ("Going back to directory : ", cfg.saved_dir)
    os.chdir(cfg.saved_dir)
    print_cfg()


def SaveGame (self):
    print ("Save Game")
    cfg.saved_dir = str(Path.cwd())
#    print ("Keep track of current directory : ", cfg.saved_dir)

    if (cfg.data_path.exists() != True):
        print ("No save directory exists.  Creating : ", str(cfg.data_path))
        cfg.data_path.mkdir(mode=0o700, parents=True, exist_ok=False)

#    print ("Changing directory to : ", str(cfg.data_path))
    os.chdir(str(cfg.data_path))

    print ("Saving Game to File : ", cfg.this_fn_to_save)
    with open(cfg.this_fn_to_save, mode="w") as fileout:

        json.dump([["NPATH_Save\n", 1], [cfg.borders, cfg.game_rows, cfg.game_cols], self.board], fileout, indent = 4, separators=(',', ': '))

    cfg.this_fn_to_open = cfg.this_fn_to_save
#    print ("Going back to directory : ", cfg.saved_dir)
    os.chdir(cfg.saved_dir)


def NewRandomGame(self):
    print ("New Random Game")
    cfg.new_game_rows = cfg.game_rows
    cfg.new_game_cols = cfg.game_cols
    cfg.new_borders = cfg.borders
    cfg.do_random_board = True
    cfg.show_board = 2  # reinitialize sprites and lists
def SimpleCheck (self):
#    print ("Simple Check")
    for i in range(len(self.board)):
        if (self.board[i][0] != self.board[i][1]):
            return (False)
    return (True)


def CheckBoard (self):
    print ("Check Board")
    if (SimpleCheck (self) == True):
        print("You Won!  Exact match found.  You've solved the puzzle congratulations!")
    else:
        print("You lost, no match found.  Sorry, try again.")


def DeleteSavedGame ():
    print ("Delete Saved Game")
    cfg.saved_dir = str(Path.cwd())
    #print ("Keep track of current directory : ", cfg.saved_dir)

    # check for saved games directory
    if (cfg.data_path.exists() != True):
        #print("Npath Save Game Directory Missing.  You haven't created : " + str(cfg.data_path) + " yet")
        pass
    elif (len(os.listdir(path=str(cfg.data_path))) == 0):
        #print("Npath Save Game Directory Is Empty.")
        pass
    else:
        # get rid of the saved file
        os.chdir(str(cfg.data_path))
        os.remove(str(cfg.this_fn_to_save))

    # get rid of the saved file directory
    if (cfg.data_path.exists() == True):
        os.rmdir(str(cfg.data_path))

    os.chdir(str(cfg.saved_dir))

    # check for config save directory
    if (cfg.config_path.exists() != True):
        #print("Npath Config Directory Missing.  You haven't created : " + str(cfg.config_path) + " yet")
        pass
    elif (len(os.listdir(path=str(cfg.config_path))) == 0):
        #print("Npath Config Directory Is Empty.")
        pass
    else:
        # get rid of the saved file
        os.chdir(str(cfg.config_path))
        os.remove(str(cfg.config_filename))

    # get rid of the config save file directory
    if (cfg.config_path.exists() == True):
        os.rmdir(str(cfg.config_path))

    os.chdir(str(cfg.saved_dir))


