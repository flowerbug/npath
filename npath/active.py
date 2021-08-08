#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

import pyglet
import sys


def DoLeftClickAction (self, x, x_rec, y, y_rec, win_pos):

    pass


def ActiveAreaLeftMouseClickAction (self, x, x_rec, y, y_rec, win_pos):

    self.square = win_pos
    if (win_pos in self.boards[self.show_board].active_squares):
        print ("Board : ", self.show_board, " selected ", win_pos, " which is an active square.")
        DoLeftClickAction (self, x, x_rec, y, y_rec, win_pos)
    else:
        print ("Board : ", self.show_board, " selected ", win_pos)


def ActiveAreaRightMouseClickAction (self, x, x_rec, y, y_rec, win_pos):

    self.square = win_pos
    if (win_pos in self.boards[self.show_board].active_squares):
        print ("Board : ", self.show_board, " selected ", win_pos, " which is an active square.")
        DoLeftClickAction (self, x, x_rec, y, y_rec, win_pos)
    else:
        print ("Board : ", self.show_board, " selected ", win_pos)


def ActiveAreaMouseMoveAction (self, x, x_rec, y, y_rec, win_pos):

        pass


