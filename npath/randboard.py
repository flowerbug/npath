#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

import pyglet
from pyglet.window import mouse
import random
from random import randrange, getrandbits
from time import sleep
import copy

import config as cfg


def InitRandomBoardItems (self):

    gridx = cfg.game_cols
    gridy = cfg.game_rows

    randpop = 1
    if ((self.board_squares != 0) and (self.board_squares >= 2)):
        randpop = random.getrandbits(32) % (self.board_squares // 2)

    # self.board_squares should always be at least 1
    if (randpop > self.board_squares):
        randpop = self.board_squares

    if randpop < 0:
        randpop = 0

    sprite_list_length = len(self.sprite_list)
#    print ("Length of sprite_list : ",sprite_list_length)
    while (randpop > 0):
        position = random.getrandbits(32) % self.board_squares
#            print ("randpop, position", randpop, position)

        if (self.board[position][0] == 0):
            randchance = random.getrandbits(32) % sprite_list_length
#            print ("  randchance", randchance)

            if (self.board[position][0] == 0):
                self.board[position][0] = randchance

        randpop -= 1

#    print (self.board)


