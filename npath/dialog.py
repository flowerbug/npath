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

from board import ClearAndResizeBoard
from version import GetVersion


# print configuration parameters
def print_cfg ():
    print ("Config Values")
    print ("Current    Borders : %-5s" %cfg.borders, "  Cols, Rows : ", cfg.game_cols, cfg.game_rows)
    print ("New        Borders : %-5s" %cfg.new_borders, "  Cols, Rows : ", cfg.new_game_cols, cfg.new_game_rows)
    print ("Defaults   Borders : %-5s" %cfg.default_borders, "  Cols, Rows : ", cfg.default_game_cols, cfg.default_game_rows)


def LoadConfigOrUseCurrent ():
    print("Load Config Or Use Current")
    if (cfg.full_config_filename.exists() == True):
        with open(cfg.full_config_filename, "r") as fn:
            loaded_config = json.load(fn)
            cfg.default_game_cols = loaded_config[1][0]
            cfg.default_game_rows = loaded_config[1][1]
            cfg.default_borders = loaded_config[1][2]
            cfg.game_cols = loaded_config[2][0]
            cfg.game_rows = loaded_config[2][1]
            if (cfg.show_board != 2):
                print("Npath Configuration Loaded")

    else:
        # current defaults are set in config.py
        # and we don't want to clobber or reset
        # them unless the user specifically requests it
        if (cfg.show_board != 2):
            print("Npath Configuration File Doesn't Exist.  The current defaults are being used instead")



def SaveConfigToFile ():
    print("Save Config To File")
    if (cfg.config_path.exists() != True):
        print("Creating : ", str(cfg.config_path))
        cfg.config_path.mkdir(mode=0o700, parents=True, exist_ok=False)
        print("Npath No Configuration Directory Exists.  We've created " + str(cfg.config_path))

    with open(cfg.full_config_filename, mode="w") as fileout:
        json.dump([["NPATH_Config\n", 1], [cfg.default_game_cols, cfg.default_game_rows, cfg.default_borders],[cfg.game_cols, cfg.game_rows, cfg.borders]], fileout, indent = 4, separators=(',', ': '))


def ChangeLayout(self):
    print ("ChangeLayout")
    cfg.borders = not cfg.borders
    if (cfg.borders == True):
        cfg.adj_size = 2
    else:
        cfg.adj_size = 0
    cfg.show_board = 2  # reinitialize sprites and lists
    cfg.do_random_board = True


def NewRandomGame(self):
    print ("New Random Game")
    cfg.show_board = 2  # reinitialize sprites and lists
    cfg.do_random_board = True
    cfg.new_game_cols = cfg.game_cols
    cfg.new_game_rows = cfg.game_rows
    cfg.new_borders = cfg.borders
#        print_cfg ()


def RestoreConfigDefaults():
    print ("Restore Config Defaults")
    cfg.game_cols = cfg.default_game_cols
    cfg.game_rows = cfg.default_game_rows
    cfg.borders = cfg.default_borders
    if (cfg.show_board != 2):
        print("Npath configuration parameters reset now using default values")


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
        + "      It keeps configuration settings in directory : " + str(cfg.config_path) + "\n"
        + "        Configuration file name : " + cfg.config_filename + "\n"
        + "\n")
    print_cfg()
    print(
        "\n\n"
        + "    'ESC' or 'Q'        : Quit\n"
        + "                             Quitting DOES NOT save the Configuration or the Game\n"
        + "\n"
        + "    'F1', 'H', or '?'   : Help (this screen)\n"
        + "\n"
        + "    'F2'                : Show or Hide guesses\n"
        + "                             Only the 'Q', 'ESC', 'F1', 'H', or '?' keys will work when showing guesses\n"
        + "\n"
        + "    'F3'                : Restore Config To Defaults\n"
        + "    'F4'                : Load Config From File\n"
        + "                             If no file exists use the Defaults\n"
        + "    'F5'                : Save Config To File\n"
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
        + "    'F11'               : Clean Up Config and Saved Game\n"
        + "\n"
        + "\n"
        + "    'F12'               : Toggle Border\n"
        + "\n"
        + "\n"
        + "    'Arrow Keys'        : Increase or Decrease Columns and Rows\n"
        + "\n"
        + "\n"
        + "    Project Location :"
        + "    https://www.github.com/flowerbug/npath\n"
        + "\n"
        )


def Load_NPATHSave_Version_1 (self, lines_in):

    cfg.new_borders = lines_in[1][0]
    cfg.new_game_cols = lines_in[1][1]
    cfg.new_game_rows = lines_in[1][2]

    cfg.new_board = []
    cfg.new_board = copy.deepcopy(lines_in[2])

    # we're going to have to redraw the board
    # but we aren't a random board
    cfg.show_board = 2
    cfg.do_random_board = False

    print ("Load_NPATHSave_Version_1 -> new variables NB NC NR NewBoard", cfg.new_borders, cfg.new_game_cols, cfg.new_game_rows, cfg.new_board)


def LoadSavedGameFromFile (self):
    print ("Load Saved Game From File")
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
        print ("LoadSavedGameFromFile...  No file selected...")
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


def SaveGameToFile (self):
    print ("Save Game To File")
    cfg.saved_dir = str(Path.cwd())
#    print ("Keep track of current directory : ", cfg.saved_dir)

    if (cfg.data_path.exists() != True):
        print ("No save directory exists.  Creating : ", str(cfg.data_path))
        cfg.data_path.mkdir(mode=0o700, parents=True, exist_ok=False)

#    print ("Changing directory to : ", str(cfg.data_path))
    os.chdir(str(cfg.data_path))

    print ("Saving Game to File : ", cfg.this_fn_to_save)
    with open(cfg.this_fn_to_save, mode="w") as fileout:

        json.dump([["NPATH_Save\n", 1], [cfg.borders, cfg.game_cols, cfg.game_rows], self.board], fileout, indent = 4, separators=(',', ': '))

    cfg.this_fn_to_open = cfg.this_fn_to_save
#    print ("Going back to directory : ", cfg.saved_dir)
    os.chdir(cfg.saved_dir)


def CleanUpConfigAndSavedGame ():
    print ("Clean Up Config And Saved Game")
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

