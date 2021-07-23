#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

import copy
import os
import random

import pyglet

import config as cfg

from dialog import LoadConfigOrUseCurrent


def MyInitStuff (self):

    random.seed()

    self.set_visible(False)

    self.png_path = cfg.png_path

    # screens, sizes and locations
    #   some of these change as the board changes size
    self.top_display = pyglet.canvas.get_display()
    self.top_screen = self.top_display.get_default_screen()
    self.full_screen_width = self.top_screen.width
    self.full_screen_height = self.top_screen.height
    print ("Full Window Size : ", self.full_screen_width, self.full_screen_height)
    self.windows_lst = self.top_display.get_windows()
    self.screen_width = self.windows_lst[0].width
    self.screen_height = self.windows_lst[0].height
    self.x, self.y = self.windows_lst[0].get_location()
    print ("WL[0] Location and Size : ", self.x, self.y, self.screen_width, self.screen_height)

    # initial window is blank and flickers i don't want 
    # to see it until it is resized later
    self.windows_lst[0].set_visible(False)

    # if there's a config file use it
    #  if there isn't set defaults specified in config.py
    LoadConfigOrUseCurrent ()

    # other useful constants
    self.board_squares = cfg.game_rows*cfg.game_cols
    self.window_cols = (cfg.game_cols+2)
    self.window_rows = (cfg.game_rows+2)
    self.window_squares = self.window_rows*self.window_cols

    self.game_board_x_limit = 0
    self.game_board_y_limit = 0

    self.keys_held = []
    self.key = pyglet.window.key

    self.mouse_win_pos = 0

    self.fps = pyglet.window.FPSDisplay(self)

    # batches for rendering
    self.fixed_batch = pyglet.graphics.Batch()
    self.fixed_board_batch = pyglet.graphics.Batch()
    self.variable_board_batch = pyglet.graphics.Batch()
    self.variable_guess_batch = pyglet.graphics.Batch()
    self.pointer_bottom_batch = pyglet.graphics.Batch()
    self.pointer_top_batch = pyglet.graphics.Batch()
    self.arrow_batch = pyglet.graphics.Batch()
    self.marble_batch = pyglet.graphics.Batch()

    # colors need precedence order for arrows
    #   we only use as many colors to mark arrows we keep in history
    self.history_limit = 6
    self.color_batch_list = []
    for i in range(self.history_limit):
        self.color_batch_list.append(pyglet.graphics.Batch())

    # lists of sprites
    self.fixed_sprites = []
    self.fixed_board_sprites = []
    self.board_sprites = []
    self.guess_sprites = []
    self.top_sprites = []

    self.white_active_squares = []
    self.white_active_squares_position = []
    self.guess_active_squares = []
    self.guess_active_squares_position = []
    self.board_to_window_index = []

    # background images : gray, white, blue
    self.game_bg_image = pyglet.image.SolidColorImagePattern(color=(211,211,211,255)).create_image(width=cfg.img_pix, height=cfg.img_pix)
    self.white_bg_image = pyglet.image.SolidColorImagePattern(color=(255,255,255,255)).create_image(width=cfg.img_pix, height=cfg.img_pix)
    self.blue_bg_image = pyglet.image.SolidColorImagePattern(color=(173,216,230,255)).create_image(width=cfg.img_pix, height=cfg.img_pix)

    self.game_tile_image = pyglet.image.load(self.png_path + "misc/tile.png")

    self.gcube_image = pyglet.image.load(self.png_path + "misc/gcube.png")
    self.cube_image  = pyglet.image.load(self.png_path + "misc/cube.png")

    self.sprite_list = []
    sprite = pyglet.sprite.Sprite(self.game_tile_image)
    self.sprite_list.append([0, self.game_tile_image, sprite, 0, 0])
    for i in range(len(cfg.color_list)):
        image = pyglet.image.SolidColorImagePattern(color=cfg.color_list[i]).create_image(width=cfg.img_pix, height=cfg.img_pix)
        sprite = pyglet.sprite.Sprite(image)
        self.sprite_list.append([0, image, sprite, 0, 0])

