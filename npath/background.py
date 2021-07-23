#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

import pyglet
import copy

import config as cfg


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
