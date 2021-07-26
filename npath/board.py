#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

import pyglet
import copy
from time import sleep

import config as cfg

from randboard import InitRandomBoardItems


# print configuration parameters
def print_cfg ():
    print ("Config Values")
    print ("Current    Borders : %-5s" %cfg.borders, "  Rows, Cols : ", cfg.game_rows, cfg.game_cols)
    print ("New        Borders : %-5s" %cfg.new_borders, "  Rows, Cols : ", cfg.new_game_rows, cfg.new_game_cols)
    print ("Defaults   Borders : %-5s" %cfg.default_borders, "  Rows, Cols : ", cfg.default_game_rows, cfg.default_game_cols)


def DrawBordersAndBackgrounds (self):

    # draw four blue corner squares
    y_pos = 0
    x_pos = 0
    x_pos_right = cfg.img_pix * (cfg.game_cols+1)
    self.fixed_sprites.append( pyglet.sprite.Sprite( self.blue_bg_image, batch=self.fixed_batch, x = x_pos, y = y_pos))
    self.fixed_sprites.append( pyglet.sprite.Sprite( self.blue_bg_image, batch=self.fixed_batch, x = x_pos_right, y = y_pos))
    y_pos = cfg.img_pix * (cfg.game_rows+1)
    self.fixed_sprites.append( pyglet.sprite.Sprite( self.blue_bg_image, batch=self.fixed_batch, x = x_pos, y = y_pos))
    self.fixed_sprites.append( pyglet.sprite.Sprite( self.blue_bg_image, batch=self.fixed_batch, x = x_pos_right, y = y_pos))

    # draw white game border
    self.white_active_squares = []
    self.white_active_squares_position = []
    y_pos = cfg.img_pix
    x_pos = 0
    x_pos_right = cfg.img_pix * (cfg.game_cols+1)
    for y in range(cfg.game_rows):
        self.fixed_sprites.append( pyglet.sprite.Sprite( self.white_bg_image, batch=self.fixed_batch, x = x_pos, y = y_pos))
        self.white_active_squares.append((self.window_cols * (y_pos // cfg.img_pix)))
        self.white_active_squares_position.append([x_pos,y_pos])
        self.fixed_sprites.append( pyglet.sprite.Sprite( self.white_bg_image, batch=self.fixed_batch, x = x_pos_right, y = y_pos))
        self.white_active_squares.append((self.window_cols * (y_pos // cfg.img_pix))+cfg.game_cols+1)
        self.white_active_squares_position.append([x_pos_right,y_pos])
        y_pos += cfg.img_pix
    y_pos = 0
    x_pos = cfg.img_pix
    y_pos_up = cfg.img_pix * (cfg.game_rows+1)
    for x in range(cfg.game_cols):
        self.fixed_sprites.append( pyglet.sprite.Sprite( self.white_bg_image, batch=self.fixed_batch, x = x_pos, y = y_pos))
        self.white_active_squares.append(x+1)
        self.white_active_squares_position.append([x_pos,y_pos])
        self.fixed_sprites.append( pyglet.sprite.Sprite( self.white_bg_image, batch=self.fixed_batch, x = x_pos, y = y_pos_up))
        self.white_active_squares.append(((self.window_rows-1) * self.window_cols)+x+1)
        self.white_active_squares_position.append([x_pos,y_pos_up])
        x_pos += cfg.img_pix
#    print ("White active squares", self.white_active_squares)
#    print ("White active square positions", self.white_active_squares_position)


def RestartGame (self):

    print ("Restart Game")

    # clear guesses
    value = len(self.board)
    for i in range(value):
        self.board[i][1] = 0

    # make any guess sprites look like the background
    if (len(self.guess_sprites) != 0):
        for j in range(len(self.guess_sprites)):
            self.guess_sprites[j].image = self.game_tile_image


def ClearBoard (self):

    # delete old board and set up new one, but
    #   DrawBoard really gets rid of all the various 
    #   lists,sprites and indexes
    try:
        del self.board
    except AttributeError:
        pass
    self.board = []

    self.board = [[0 for i in range(2)] for j in range(self.board_squares)]


def ResizeBoard (self):

    # ok, let's see...
    #self.set_visible(True)

    # where are we now
    self.game_x, self.game_y = self.get_location()
    print ("Previous WL[0]  Location          : ", self.game_x, self.game_y, "  Size : ", self.screen_width, self.screen_height)

    if (cfg.borders == True):
        cfg.adj_size = 2
    else:
        cfg.adj_size = 0
    self.window_rows = (cfg.game_rows+cfg.adj_size)
    self.window_cols = (cfg.game_cols+cfg.adj_size)
    self.board_squares = cfg.game_rows*cfg.game_cols
    self.window_squares = self.window_rows*self.window_cols

    # have to have at least one
    if (self.window_squares < 1):
        self.window_rows = 1
        self.window_cols = 1
        self.window_squares = 1

    # adjust the main window size to fit

    self.screen_width = (self.window_cols * cfg.img_pix)
    self.screen_height = (self.window_rows * cfg.img_pix)

    self.game_x = (self.full_screen_width - self.screen_width) // 2
    self.game_y = (self.full_screen_height - self.screen_height) // 2

    self.set_location(self.game_x, self.game_y)
    self.set_size(self.screen_width, self.screen_height)

    print ("Moved and Resized WL[0]  Location : ", self.game_x, self.game_y, "  Size : ", self.screen_width, self.screen_height)

    # ok, let's see...
    self.set_visible(True)

    # attempt to restore keyboard focus to the window
    self.activate()


def DrawBoard (self):

    if (cfg.show_board == 2):

        print_cfg ()
        self.cube.visible = False
        self.gcube.visible = False

        # clear the sprites and lookup tables from the previous board

        if (len(self.fixed_sprites) != 0):
            for j in range(len(self.fixed_sprites)):
                #self.fixed_sprites[j].visible = False
                self.fixed_sprites[j].delete()
            del self.fixed_sprites
            self.fixed_sprites = []

        if (len(self.white_active_squares) != 0):
            del self.white_active_squares
            self.white_active_squares = []

        if (len(self.white_active_squares_position) != 0):
            del self.white_active_squares_position
            self.white_active_squares_position = []

        if (len(self.board_sprites) != 0):
            for j in range(len(self.board_sprites)):
                #self.board_sprites[j].visible = False
                self.board_sprites[j].delete()
            del self.board_sprites
            self.board_sprites = []

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
            ResizeBoard (self)
            ClearBoard (self)
            InitRandomBoardItems (self)
            cfg.do_random_board = False
        else:

            # it is a restarted game or newly loaded board
            if (cfg.new_game_rows == None):

                # we don't change a restarted game
                pass

            else:  # it is a newly loaded board
                print ("DrawBoard Draw Newly Loaded Board")
                cfg.game_rows = cfg.new_game_rows
                cfg.game_cols = cfg.new_game_cols
                cfg.borders = cfg.new_borders
                ClearBoard (self)
                self.board = copy.deepcopy(cfg.new_board)
                print ("DrawBoard cfg.new_board : ", cfg.new_board)
                print ("DrawBoard self.board : ", self.board)
                cfg.new_game_rows = None
                cfg.new_game_cols = None
                cfg.new_borders = None
                try:
                   del self.new_board
                except AttributeError:
                   pass
                if (cfg.borders == True):
                   cfg.adj_size = 2
                else:
                   cfg.adj_size = 0
                ResizeBoard (self)

        print_cfg ()

        # in all cases
        if (cfg.borders == True):
            DrawBordersAndBackgrounds (self)

        print_cfg ()

        # draw game grid
        print ("DrawBoard show board : ", cfg.show_board, "  borders : ", cfg.borders)
        print ("DrawBoard initial board start : ", self.board)
        if (cfg.borders == True):
            x_pos = cfg.img_pix
            y_pos = cfg.img_pix
            self.game_board_x_lower_limit = x_pos
            self.game_board_y_lower_limit = y_pos
            win_pos = self.window_cols + 1
        else:
            x_pos = 0
            y_pos = 0
            self.game_board_x_lower_limit = x_pos
            self.game_board_y_lower_limit = y_pos
            win_pos = 0


        for x in range(cfg.game_rows):
            x_pos = self.game_board_x_lower_limit
            for y in range(cfg.game_cols):
                board_position = (cfg.game_cols * x) + y
                print ("BP WP x y: ", board_position, win_pos, x, y)
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
            if (cfg.borders == True):
               win_pos += 2
        self.game_board_x_upper_limit = x_pos
        self.game_board_y_upper_limit = y_pos
        cfg.show_board = 1

#        print ("Guess active squares", self.guess_active_squares)
#        print ("Guess active square positions", self.guess_active_squares_position)
#        print ("board_to_window_index", self.board_to_window_index)
#        print ("game board limits ", self.game_board_x_lower_limit, self.game_board_x_upper_limit,
#            self.game_board_y_lower_limit, self.game_board_y_upper_limit)
        print ("DrawBoard board initial board finish : ", self.board)

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


