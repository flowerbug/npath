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
    if (self.show_board == 1):
        if (win_pos in self.white_active_squares):
#            print ("selected ", win_pos, " which is an active White square.")
            DoLeftClickAction (self, x, x_rec, y, y_rec, win_pos)
        else:
            pass


def ActiveAreaRightMouseClickAction (self, x, x_rec, y, y_rec, win_pos):

    self.square = win_pos
    if (self.show_board == 1):
        if (win_pos in self.white_active_squares):
#            print ("selected ", win_pos, " which is an active White square.")
            pass
        else:
            pass


def ActiveAreaMouseMoveAction (self, x, x_rec, y, y_rec, win_pos):

        pass


