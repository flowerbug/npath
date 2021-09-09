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

from board import Board
from version import GetVersion


# print configuration parameters
def print_cfg (self):
    print ("Config Values")
    print ("Current    Rows, Cols : ", self.game_rows, self.game_cols)


def ShowAbout (self):
    print(
        "\n    Npath is running in directory : " + str(Path.cwd()) + "\n"
        "    Npath code is running from directory : " + os.path.dirname(__file__) + "\n"
        + "\n"
        + "      It saves game files to directory : " + str(self.data_path) + "\n"
        + "\n"
        "    Npath Version is : " + GetVersion() + "\n"
        + "\n"
        + "        Open file name : " + str(self.this_fn_to_open) + "\n"
        + "        Save file name : " + str(self.this_fn_to_save) + "\n"
        + "\n"
        + "\n"
        + "      It keeps the configuration settings with the saved game.\n"
        + "\n")
    print_cfg(self)
    print(
        "\n\n"
        + "    'ESC' or 'Q'        : Quit\n"
        + "                             Quitting DOES NOT save the Game\n"
        + "\n"
        + "    'F1', 'H', or '?'   : Help (this screen)\n"
        + "\n"
        + "    'F2'                : Show or Hide Boards\n"
        #+ "                             Only the 'Q', 'ESC', 'F1', 'H', or '?' keys will work when showing guesses\n"
        + "\n"
        + "\n"
        + "    'F4'                : Toggle Mouse Drag Resizing\n"
        + "                              Pressing and holding a mouse key will either \n"
        + "                              increase or decrease the size as long as you \n"
        + "                              hold the key down, but remember to release the \n"
        + "                              key if you want to go back the other direction \n"
        + "\n"
        + "\n"
        + "    'Arrow Keys'        : Increase or Decrease Columns and Rows\n"
        + "\n"
        + "    NumPad '+' '-' Keys : Increase or Decrease Tile Size\n"
        + "\n"
        + "\n"
        + "    'F6'                : Load Game From File\n"
        + "    'F7'                : Save Game To File\n"
        + "\n"
        + "    'F8'                : New Random Game\n"
        + "\n"
        + "    'F9'                : 1 Column x 1 Row Maximum Size Tile\n"
        + "                             With 8x Magnified Corners\n"
        + "\n"
        + "    'F10'               : Check Game\n"
        + "                             To see if we've won\n"
        + "\n"
        + "\n"
        + "    'F11'               : Delete Saved Game and Directory\n"
        + "\n"
        + "\n"
        + "    'P'                 : Print the Image Numbers of the Board\n"
        + "\n"
        + "    'B'                 : Toggle Through the Button Styles If the\n"
        + "                             Tile Was Not Loaded from a File\n"
        + "\n"
        + "\n"
        + "    Project Location :"
        + "    https://www.github.com/flowerbug/npath\n"
        + "\n"
        )


def ChangeLayout(self):
    print ("ChangeLayout")


def Load_NPATH_Version_1 (self, lines_in):

    self.game_rows = lines_in[1][0]
    self.game_cols = lines_in[1][1]

    #print(lines_in[1])
    #print(lines_in[2])
    #print(lines_in[3])
    print ("Length self.boards : ", len(self.boards))
    if (len(self.boards) != 0):
        for x in len(self.boards):
            self.boards[x].delete()
        del self.boards
        self.boards = []
    self.boards.append(Board(self, self.game_rows, self.game_cols, self.img_pix, self.img_pix, False, lines_in[2], self.over_batch, self.foreground_board_group))
    self.boards.append(Board(self, self.game_rows, self.game_cols, self.img_pix, self.img_pix, False, lines_in[3], self.under_batch, self.background_board_group))
    #print ("Load_NPATH_Version_1 -> new values for : R C NB NM", self.game_rows, self.game_cols, self.boards[0], self.boards[1])


def LoadGame (self):
    print ("Load Game")
    self.saved_dir = str(Path.cwd())
    #print ("Keep track of current directory : ", self.saved_dir)

    # check for saved games directory
    if (self.data_path.exists() != True):
        print("No Saved Game To Load.")
        return

    # is there anything in there?
    if (len(os.listdir(path=str(self.data_path))) == 0):
        print("Saved Game Directory Is Empty.")
        return

    #print ("Changing directory to : ", str(self.data_path))
    os.chdir(str(self.data_path))

    if (self.this_fn_to_open == None):
        print ("LoadGame...  No file selected...")
        os.chdir(self.saved_dir)
        return

    if (self.this_fn_to_open.endswith(".json") == True):
        with open(self.this_fn_to_open) as filein:
            lines_in = json.load(filein)
            Load_NPATH_Version_1 (self, lines_in)
            self.do_random_board = False
            self.this_fn_to_save = self.this_fn_to_open
            #print ("fn : ", self.this_fn_to_open, " lines in : ", lines_in)

    #print ("Going back to directory : ", self.saved_dir)
    os.chdir(self.saved_dir)
    #print_cfg(self)


def SaveGame (self):
    print ("Save Game")
    self.saved_dir = str(Path.cwd())
    #print ("Keep track of current directory : ", self.saved_dir)

    if (self.data_path.exists() != True):
        print ("No save directory exists.  Creating : ", str(self.data_path))
        self.data_path.mkdir(mode=0o700, parents=True, exist_ok=False)

    #print ("Changing directory to : ", str(self.data_path))
    os.chdir(str(self.data_path))

    print ("Saving Game to File : ", self.this_fn_to_save)
    with open(self.this_fn_to_save, mode="w") as fileout:

        json.dump([["NPATH_Save\n", 1], [self.game_rows, self.game_cols], self.boards[0].num_list(), self.boards[1].num_list()], fileout, indent = 4, separators=(',', ': '))

    print ("Saved Game to File")
    self.this_fn_to_open = self.this_fn_to_save
    #print ("Going back to directory : ", self.saved_dir)
    os.chdir(self.saved_dir)


def SimpleCheck (self):
    #print ("Simple Check")
    for i in range(len(self.boards[0].tiles)):
        if (self.boards[0].tiles[i] != self.boards[1].tiles[i]):
            return (False)
    return (True)


def CheckBoard (self):
    print ("Check Board")
    if (SimpleCheck (self) == True):
        print("You Won!  Exact match found.  You've solved the puzzle congratulations!")
    else:
        print("You lost, no match found.  Sorry, try again.")


def DeleteSavedGame (self):
    print ("Delete Saved Game")
    self.saved_dir = str(Path.cwd())
    #print ("Keep track of current directory : ", self.saved_dir)

    # check for saved games directory
    if (self.data_path.exists() != True):
        #print("Npath Save Game Directory Missing.  You haven't created : " + str(self.data_path) + " yet")
        pass
    elif (len(os.listdir(path=str(self.data_path))) == 0):
        #print("Npath Save Game Directory Is Empty.")
        pass
    else:
        # get rid of the saved file
        os.chdir(str(self.data_path))
        os.remove(str(self.this_fn_to_save))

    # get rid of the saved file directory
    #if (self.data_path.exists() == True):
    #    os.rmdir(str(self.data_path))

    os.chdir(str(self.saved_dir))


