#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

import random
from time import sleep

import pyglet
import copy


class Tile ():


    def __init__ (self, window, tile_img_number, tile_height, tile_width, tile_x, tile_y, batch, group):
        self.img_number = tile_img_number
        if ((self.img_number == None) or (self.img_number < 0) or self.img_number > len(window.sprite_list)):
            img = window.sprite_list[0][0]
        else:
            img = window.sprite_list[self.img_number][0]
        self.spr = pyglet.sprite.Sprite(img, 0, 0)
        self.spr.x = tile_x
        self.spr.y = tile_y
        self.spr.batch = batch
        self.spr.group = group
        self.spr.visible = True


    def delete (self):
        self.spr.delete()


    def set_img (self, img_number, img):
        self.img_number = img_number
        self.spr.image = img


class Board ():

    def __init__ (self, window, height, width, tile_height, tile_width, random_board, loaded_board, batch, group):
        self.board_height = height
        self.board_width = width
        self.tile_height = tile_height
        self.tile_width = tile_width
        self.is_random_board = random_board
        self.do_random_board = random_board
        self.do_loaded_board = copy.deepcopy(loaded_board)
        self.batch = batch
        self.group = group
        self.active_squares = [len(window.boards)]

        # make a board of the right size and fill it with the base tile
        # from the sprite list
        self.tiles = []
        for y in range (height):
            for x in range (width):
                self.tiles.append (Tile (window, 0, self.tile_height, self.tile_width, 0, 0, self.batch, self.group))
                self.tiles[-1].spr.x = x * self.tile_width
                self.tiles[-1].spr.y = y * self.tile_height
                self.tiles[-1].spr.visible = True

        # if it is a random board replace the base tiles
        if (self.do_random_board == True):
            #print ("Random Board in Class Board")
            self.bd_randomize (window)
            self.do_random_board = False

        # if it is a board to create from a list use those numbers instead
        elif (self.do_loaded_board != None):
            #print ("Loaded Board in Class Board", self.do_loaded_board)
            if (len(self.do_loaded_board) == len(self.tiles)):
                for x in range(len(self.do_loaded_board)):
                    self.tiles[x].set_img (self.do_loaded_board[x], window.sprite_list[self.do_loaded_board[x]][0])
            else:
                print("Class Board : Lengths don't match?")
            self.do_loaded_board = None


    def __str__ (self):
        num_str = ""
        num_str = " ".join(self.num_str_list())
        return f"Board :  Height : {self.board_height}  Width : {self.board_width}\n  Batch : {self.batch}  Group : {self.group}\n  Tiles : {num_str}"


    def num_str_list (self):
        tiles_num_str_list = []
        for x in range(len(self.tiles)):
            tiles_num_str_list.append(str(self.tiles[x].img_number))
        return (tiles_num_str_list)


    def num_list (self):
        tiles_num_list = []
        for x in range(len(self.tiles)):
            tiles_num_list.append(self.tiles[x].img_number)
        return (tiles_num_list)


    def delete (self):
        for x in range(len(self.tiles)):
            self.tiles[0].spr.delete()


    def set_all (self, img_number, img):
        for x in range(len(self.tiles)):
            self.tiles[x].set_img (img_number, img)


    def bd_sparse_randomize (self, window):

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
        sprite_list_length = len(window.sprite_list)
        placed = 0
        while (randpop > 0):
            position = random.getrandbits(32) % window.board_squares
            #print ("randpop, position", randpop, position)

            if (self.tiles[position].img_number == 0):

                # don't pick 0 since that's the foreground blank tile image
                randchance = random.randint(1,100)
                if (randchance < sprite_list_length):
                    placed += 1
                    #print ("Position : ", position, " Img : ", randchance)
                    self.tiles[position].set_img (randchance, window.sprite_list[randchance][0])
            randpop -= 1

        #print (" Placed : ", placed)


    def bd_randomize (self, window):

        # fill all the squares
        sprite_list_length = len(window.sprite_list) - 1
        for x in range(len(self.tiles)):
            # don't pick 0 since that's the foreground blank tile image
            randchance = random.randint(1,sprite_list_length)
            self.tiles[x].set_img (randchance, window.sprite_list[randchance][0])


    def add_row (self, window):

        #print ("Add Row  BH  : ", self.board_height)
        y = self.board_height
        for x in range(self.board_width):
            if (self.is_random_board == False):
                self.tiles.append (Tile (window, 0, self.tile_height, self.tile_width, 0, 0, self.batch, self.group))
                self.tiles[-1].spr.x = x * self.tile_width
                self.tiles[-1].spr.y = y * self.tile_height
                self.tiles[-1].spr.visible = True

            else:
                self.tiles.append (Tile (window, 0, self.tile_height, self.tile_width, 0, 0, self.batch, self.group))
                randchance = random.randint (1, len (window.sprite_list) - 1)
                self.tiles[-1].set_img (randchance, window.sprite_list[randchance][0])
                self.tiles[-1].spr.x = x * self.tile_width
                self.tiles[-1].spr.y = y * self.tile_height
                self.tiles[-1].spr.visible = True

        self.board_height += 1
        #print (self)


    def add_col (self, window):

        #print (self)
        tile_ind = len(self.tiles)
        x = self.board_width
        for y in range(self.board_height-1, -1, -1):
            #print (" X Y ind : ", x, y, tile_ind)
            if (self.is_random_board == False):
                self.tiles.insert (tile_ind, Tile (window, 0, self.tile_height, self.tile_width, 0, 0, self.batch, self.group))
                self.tiles[tile_ind].spr.x = x * self.tile_width
                self.tiles[tile_ind].spr.y = y * self.tile_height
                self.tiles[tile_ind].spr.visible = True
            else:
                self.tiles.insert (tile_ind, Tile (window, 0, self.tile_height, self.tile_width, 0, 0, self.batch, self.group))
                randchance = random.randint (1, len (window.sprite_list) - 1)
                self.tiles[tile_ind].set_img (randchance, window.sprite_list[randchance][0])
                self.tiles[tile_ind].spr.x = x * self.tile_width
                self.tiles[tile_ind].spr.y = y * self.tile_height
                self.tiles[tile_ind].spr.visible = True
            tile_ind -= self.board_width
            y -= 1

        self.board_width += 1
        #print (self)


    def del_row (self, window):

        #print (self)
        del self.tiles[-self.board_width:]
        self.board_height -= 1
        #print (self)


    def del_col (self, window):

        #print (self)
        del self.tiles[self.board_width-1:len(self.tiles):self.board_width]
        self.board_width -= 1
        #print (self)


    def resize (self, window, key):

        if (key == None):
            return

        old_size = len(self.tiles)

        if (key == pyglet.window.key.LEFT):
            new_rows = window.game_rows
            new_cols = window.game_cols - 1
        elif (key == pyglet.window.key.RIGHT):
            new_rows = window.game_rows
            new_cols = window.game_cols + 1
        elif (key == pyglet.window.key.UP):
            new_rows = window.game_rows + 1
            new_cols = window.game_cols
        elif (key == pyglet.window.key.DOWN):
            new_rows = window.game_rows - 1
            new_cols = window.game_cols
        new_size = new_rows * new_cols

        if (new_size == old_size):
            return
        elif (new_size > old_size):
            if (key == pyglet.window.key.RIGHT):
                self.add_col (window)
            elif (key == pyglet.window.key.UP):
                self.add_row (window)
        else:
            if (key == pyglet.window.key.LEFT):
                self.del_col (window)
            elif (key == pyglet.window.key.DOWN):
                self.del_row (window)


