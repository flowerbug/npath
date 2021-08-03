#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

import random
from time import sleep

import pyglet
import copy


def bd_random_board (self, window):

    randpop = 1
    if ((window.board_squares != 0) and (window.board_squares >= 2)):
        randpop = random.getrandbits(32) % window.board_squares
        randpop = randpop * 100

    # window.board_squares should always be at least 1
    if (randpop > window.board_squares):
        randpop = window.board_squares

    if randpop < 0:
        randpop = 1

    # window.sprite_list is how many colors to be used
    #   as a percentage, but you can add more to randpop
    #   to fill in the board even further.  if you want to
    #   weight certain colors higher duplicate those colors 
    #   in window.color_list.
    #
    #   for this version i want a full board of random 
    #   colors (duplicates allowed) so i use placed as
    #   the limit.
    sprite_list_length = len(window.sprite_list)
    placed = 0
    while ((randpop > 0) or (placed < window.board_squares)):
        position = random.getrandbits(32) % window.board_squares
        #print ("randpop, position", randpop, position)

        if (self.tiles[position].img_number == 0):

            # don't pick 0 since that's the foreground blank tile image
            randchance = random.randint(1,100)
            if (randchance < sprite_list_length):
                placed += 1
                #print ("Position : ", position, " Img : ", randchance)
                self.tiles[position].img_number = randchance
                self.tiles[position].img = window.sprite_list[randchance][0]
                self.tiles[position].spr.image = window.sprite_list[randchance][0]
        randpop -= 1

    #print (" Placed : ", placed)


class Tile ():

    def __init__(self, window, tile_img_number, tile_height, tile_width, tile_x, tile_y, batch, group):
        self.img_number = tile_img_number
        if ((self.img_number == None) or (self.img_number < 0) or self.img_number > len(window.sprite_list)):
            self.img = window.sprite_list[0][0]
        else:
            self.img = window.sprite_list[self.img_number][0]
        self.spr = pyglet.sprite.Sprite(self.img, 0, 0)
        self.spr.x = tile_x
        self.spr.y = tile_y
        self.spr.batch = batch
        self.spr.group = group
        self.spr.visible = True

    def delete (self):
        self.spr.delete()


class Board ():

    def __init__(self, window, height, width, tile_height, tile_width, random_board, batch, group):
        self.board_height = height
        self.board_width = width
        self.tile_height = tile_height
        self.tile_width = tile_width
        self.do_random_board = random_board
        self.batch = batch
        self.group = group
        self.tiles = []
        if (height <= 0):
            height = 1
        if (width <= 0):
            width = 1
        if (tile_height <= 0):
            tile_height = 1
        if (tile_width <= 0):
            tile_width = 1

        # make a board of the right size and fill it with the base tile
        # from the sprite list
        for y in range (height):
            for x in range (width):
                tile_c = Tile(window, 0, self.tile_height, self.tile_width, 0, 0, self.batch, self.group)
                self.tiles.append (tile_c)
                self.tiles[-1].spr.x = x * self.tile_width
                self.tiles[-1].spr.y = y * self.tile_height
                self.tiles[-1].spr.visible = True

        # if it is a random board replace the base tiles
        if (self.do_random_board == True):
            bd_random_board (self, window)
            self.do_random_board = False

    def __str__(self):
        tiles_str = ""
        for x in range(len(self.tiles)):
            tiles_str = tiles_str + " " + str(self.tiles[x].img_number)
        return f"\nBoard :  Height : {self.board_height}  Width : {self.board_width}\n  Batch : {self.batch}  Group : {self.group}\n  Tiles : {tiles_str}\n"

    def delete (self):
        for x in range(len(self.tiles)):
            self.tiles[0].spr.delete()


def RestartGame (self):

    print ("Restart Game")


def ClearBoard (self):

    print ("Clear Board")


def ResizeBoard (self):

    print ("Resize Board")

    # ok, let's see...
    self.set_visible(True)

    # where are we now
    self.game_x, self.game_y = self.get_location()
    print ("Previous WL[0]  Location          : ", self.game_x, self.game_y, "  Size : ", self.screen_width, self.screen_height)

    self.window_rows = self.game_rows
    self.window_cols = self.game_cols
    self.board_squares = self.game_rows*self.game_cols
    self.window_squares = self.window_rows*self.window_cols

    # have to have at least one
    if (self.window_squares < 1):
        self.window_rows = 1
        self.window_cols = 1
        self.window_squares = 1

    # adjust the main window size to fit

    self.screen_width = (self.window_cols * self.img_pix)
    self.screen_height = (self.window_rows * self.img_pix)

    self.game_x = (self.full_screen_width - self.screen_width) // 2
    self.game_y = (self.full_screen_height - self.screen_height) // 2

    self.set_location(self.game_x, self.game_y)
    self.set_size(self.screen_width, self.screen_height)

    print ("Moved and Resized WL[0]  Location : ", self.game_x, self.game_y, "  Size : ", self.screen_width, self.screen_height)

    # ok, let's see...
    self.set_visible(True)

    # attempt to restore keyboard focus to the window
    self.activate()
