#!/usr/bin/env python3 
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

import pyglet
import sys

import config as cfg

from marbles import DoLeftClickWhiteAction


def ActiveAreaLeftMouseClickAction (self, x, x_rec, y, y_rec, win_pos):

    cfg.square = win_pos
    if (cfg.show_board == 1):
        if (win_pos in self.white_active_squares):
#            print ("selected ", win_pos, " which is an active White square.")
            DoLeftClickWhiteAction (self, x, x_rec, y, y_rec, win_pos)
        else:
            pass


def ActiveAreaRightMouseClickAction (self, x, x_rec, y, y_rec, win_pos):

    cfg.square = win_pos
    if (cfg.show_board == 1):
        if (win_pos in self.white_active_squares):
#            print ("selected ", win_pos, " which is an active White square.")
            pass
        else:
            pass


def ActiveAreaMouseMoveAction (self, x, x_rec, y, y_rec, win_pos):

        pass


