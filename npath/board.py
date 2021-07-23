#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

import pyglet
import copy
from time import sleep

import config as cfg

from background import DrawBordersAndBackgrounds
from randboard import InitRandomBoardItems


def RestartGame (self):

    print ("Restart Game")

    # clear guesses
    value = len(self.board)
    for i in range(value):
        self.board[i][1] = 0

    # make any guess sprites look like the background
    if (len(self.guess_sprites) != 0):
        for j in range(len(self.guess_sprites)):
            self.guess_sprites[j].image = self.game_bg_image


def ClearAndResizeBoard (self):


    # ok, let's see...
    self.set_visible(True)

    # use the current cfg values
    self.board_squares = cfg.game_rows*cfg.game_cols
    self.window_rows = (cfg.game_rows+2)
    self.window_cols = (cfg.game_cols+2)
    self.window_squares = self.window_rows*self.window_cols

    # adjust the main window size to fit

    self.screen_width = (self.window_cols * cfg.img_pix)
    self.screen_height = (self.window_rows * cfg.img_pix)

    self.game_x = (self.full_screen_width - self.screen_width) // 2
    self.game_y = (self.full_screen_height - self.screen_height) // 2

    self.set_location(self.game_x, self.game_y)
    self.set_size(self.screen_width, self.screen_height)

    print ("Moved and Resized WL[0]  Location : ", self.game_x, self.game_y, "  Size : ", self.screen_width, self.screen_height)

    # ok, let's see...
#   self.set_visible(True)


    # delete old board and set up new one, but
    #   DrawBoard really gets rid of all the various 
    #   lists,sprites and indexes
    try:
        del self.board
    except AttributeError:
        pass
    self.board = []

    self.board = [[0 for i in range(2)] for j in range(self.board_squares)]

    # move the gcube
    try:
        self.gcube.x = cfg.img_pix * (cfg.game_cols+1)
    except:
        pass


def DrawBoard (self):

    if (cfg.show_board == 2):

        self.cube.visible = False
        self.gcube.visible = False

        if (len(self.fixed_sprites) != 0):
            for j in range(len(self.fixed_sprites)):
                #self.fixed_sprites[j].visible = False
                self.fixed_sprites[j].delete()
            del self.fixed_sprites
            self.fixed_sprites = []

        if (len(self.fixed_board_sprites) != 0):
            for j in range(len(self.fixed_board_sprites)):
                #self.fixed_board_sprites[j].visible = False
                self.fixed_board_sprites[j].delete()
            del self.fixed_board_sprites
            self.fixed_board_sprites = []

        if (len(self.board_sprites) != 0):
            for j in range(len(self.board_sprites)):
                #self.board_sprites[j].visible = False
                self.board_sprites[j].delete()
            del self.board_sprites
            self.board_sprites = []

        if (len(self.white_active_squares) != 0):
            del self.white_active_squares
            self.white_active_squares = []

        if (len(self.white_active_squares_position) != 0):
            del self.white_active_squares_position
            self.white_active_squares_position = []

        if (len(self.guess_sprites) != 0):
            for j in range(len(self.guess_sprites)):
                #self.guess_sprites[j].visible = False
                self.guess_sprites[j].delete()
            del self.guess_sprites
            self.guess_sprites = []

        if (len(self.guess_active_squares) != 0):
            del self.guess_active_squares
            self.guess_active_squares = []

        if (len(self.guess_active_squares_position) != 0):
            del self.guess_active_squares_position
            self.guess_active_squares_position = []

        if (len(self.board_to_window_index) != 0):
            del self.board_to_window_index
            self.board_to_window_index = []


        if (cfg.do_random_board == True):
#            print ("DrawBoard Draw Random Board")

            ClearAndResizeBoard (self)
            InitRandomBoardItems (self)
            DrawBordersAndBackgrounds (self)
            cfg.do_random_board = False
        else:
            # it's a newly loaded board
#            print ("DrawBoard Draw Loaded Board")

            cfg.game_cols = cfg.new_game_cols
            cfg.game_rows = cfg.new_game_rows
            # we use ClearAndResizeBoard to put the window on
            # the screen in the right spot
            ClearAndResizeBoard (self)
            del self.board
            self.board = copy.deepcopy(cfg.new_board)
            DrawBordersAndBackgrounds (self)

        # draw game grid
#        print ("DrawBoard show board 2", cfg.show_board)
#        print ("DrawBoard initial board start", self.board)
        y_pos = cfg.img_pix
        x_pos = cfg.img_pix
        self.game_board_x_lower_limit = x_pos
        self.game_board_y_lower_limit = y_pos
#       win_pos = ((self.window_rows - 2) * self.window_cols) + 1
        win_pos = self.window_cols + 1

        for x in range(cfg.game_rows):
            x_pos = self.game_board_x_lower_limit
            for y in range(cfg.game_cols):
                board_position = (cfg.game_cols * x) + y
#                print ("BP WP x y: ", board_position, win_pos, x, y)
                self.fixed_board_sprites.append( pyglet.sprite.Sprite( self.game_bg_image, batch=self.fixed_board_batch, x = x_pos, y = y_pos))
                image = self.sprite_list[self.board[board_position][0]][1]
                self.board_sprites.append( pyglet.sprite.Sprite( image, batch=self.variable_board_batch, x = x_pos, y = y_pos))
                image = self.sprite_list[self.board[board_position][1]][1]
                self.guess_sprites.append( pyglet.sprite.Sprite( image, batch=self.variable_guess_batch, x = x_pos, y = y_pos))
                self.guess_active_squares.append(win_pos)
                self.guess_active_squares_position.append([x_pos,y_pos])
                self.board_to_window_index.append(win_pos)
                x_pos += cfg.img_pix
                win_pos += 1
            y_pos += cfg.img_pix
            win_pos += 2
        self.game_board_x_upper_limit = x_pos
        self.game_board_y_upper_limit = y_pos
        cfg.show_board = 1

#        print ("Guess active squares", self.guess_active_squares)
#        print ("Guess active square positions", self.guess_active_squares_position)
#        print ("board_to_window_index", self.board_to_window_index)
#        print ("game board limits ", self.game_board_x_lower_limit, self.game_board_x_upper_limit,
#            self.game_board_y_lower_limit, self.game_board_y_upper_limit)
#        print ("DrawBoard board initial board finish", self.board)

    elif (cfg.show_board == 0):

        self.cube.visible = True
        self.gcube.visible = False

        for j in range(len(self.board_sprites)):
            self.board_sprites[j].visible = True
        for j in range(len(self.guess_sprites)):
            self.guess_sprites[j].visible = False
#        print ("DrawBoard draw show board 0", len(self.board_sprites), len(self.guess_sprites), cfg.show_board)

    else:

        self.cube.visible = False
        self.gcube.visible = True

        for j in range(len(self.board_sprites)):
            self.board_sprites[j].visible = False
        for j in range(len(self.guess_sprites)):
            self.guess_sprites[j].visible = True
#        print ("DrawBoard draw show board 1", len(self.board_sprites), len(self.guess_sprites), cfg.show_board)


