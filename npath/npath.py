#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

import copy, os, random
from pathlib import Path, PurePath

import pyglet
from pyglet.window import mouse
from pyglet import clock

from active import ActiveAreaLeftMouseClickAction, ActiveAreaRightMouseClickAction, ActiveAreaMouseMoveAction
from board import new_random_game, Board, ResizeBoard
from dialog import ChangeLayout, CheckBoard, DeleteSavedGame, LoadGame, SaveGame, ShowAbout
from version import GetVersion


class Window(pyglet.window.Window):


    def __init__ (
            self,
            width,
            height,
            caption,
            resizable,
            fullscreen,
            visible,
            *args,
            **kwargs):


        super(Window, self).__init__(width, height, caption, resizable, fullscreen, visible, *args, **kwargs)


        print("Pyglet version : ", pyglet.version)
        print("Npath version  : ", GetVersion())


        # the path to the images
        self.png_path = os.path.dirname(__file__) + "/graphics/"

        # colors
        self.color_list = [
            (  0,   0,   0, 255),  # black
            (255,   0,   0, 255),  # red
            (  0, 255,   0, 255),  # green
            (  0,   0, 255, 255),  # blue
            (128,   0, 128, 255),  # purple
            (255, 165,   0, 255),  # orange
            (255, 255,   0, 255),  # yellow
            (  0, 255, 255, 255),  # cyan
            (255,   0, 255, 255),  # fuchia
            (255, 192, 203, 255),  # pink
            ( 34, 139,  34, 255),  # forestgreen
            (211, 211, 211, 255),  # lightgray
            (160,  82,  45, 255),  # sienna
            (128, 128, 128, 255),  # gray
            ( 65, 105, 225, 255),  # royalblue
            (135, 206, 235, 255),  # skyblue
            (  0,   0, 139, 255),  # darkblue
            (135, 135, 135, 255)
            ]

        #   save game location and initial file
        # you can always save/load other names, 
        # this is just a suggestion...
        self.suggested_fn = "save.json"
        self.this_fn_to_open = self.suggested_fn
        self.this_fn_to_save = self.suggested_fn

        self.home = Path.home()
        self.saved_dir = None

        # save file directory
        if (os.name == "posix"):
            self.home = Path.home()
            self.data_path = self.home / Path(".local/share/npath")
        else:
            print ("  Npath doesn't know where to set data_path for OS : ", os.name)
            print ("This is where a user would save their games.")


        # the window, board and tile basic unit of size
        self.img_pix = 64


        # some limits and testing values

        self.min_rows = 1     # must be 1 or greater
        self.min_cols = 1     #

        self.max_rows = 50    # for temporary testing - i don't know how big
        self.max_cols = 50    #    a value i can put in here.


        # board size if no saved board exists
        self.game_rows = 3     # height
        self.game_cols = 5     # width

        # and some testing values
        #self.game_rows = 1    # height
        #self.game_cols = 1    # width
 
        # to fill the full screen in 1920 1080 with 64x64 pixel tiles
        #self.game_rows = 15   # height
        #self.game_cols = 30   # width

        #self.game_rows = 49   # height
        #self.game_cols = 49   # width


        # screens, sizes and locations
        #   some of these change as the board changes size
        self.top_display = pyglet.canvas.get_display()
        self.top_screen = self.top_display.get_default_screen()
        self.full_screen_width = self.top_screen.width
        self.full_screen_height = self.top_screen.height
        print ("Full Window Size :  ", self.full_screen_width, "x", self.full_screen_height, " pix")
        self.windows_lst = self.top_display.get_windows()
        self.wl0 = self.windows_lst[0]
        self.screen_width = self.windows_lst[0].width
        self.screen_height = self.windows_lst[0].height
        self.x, self.y = self.windows_lst[0].get_location()
        print ("WL[0] Location\n  X Y       :  ", self.x, self.y, "\n  Size      :  ", self.screen_width, self.screen_height, " pix\n  Rows Cols :  ", self.game_rows, self.game_cols)

        # initial window is blank and flickers i don't want 
        # to see it until it is resized later
        self.windows_lst[0].set_visible(False)

        # other useful constants
        self.board_squares = self.game_rows*self.game_cols
        self.window_rows = self.game_rows
        self.window_cols = self.game_cols
        self.window_squares = self.window_rows*self.window_cols

        self.keys_held = []
        self.key = pyglet.window.key

        self.mouse_win_pos = 0

        self.fps = pyglet.window.FPSDisplay(self)


        # batches for rendering
        self.batch = pyglet.graphics.Batch()
        self.over_batch = pyglet.graphics.Batch()

        self.fixed_batch = pyglet.graphics.Batch()
        self.fixed_board_batch = pyglet.graphics.Batch()
        self.pointer_bottom_batch = pyglet.graphics.Batch()
        self.pointer_middle_batch = pyglet.graphics.Batch()
        self.pointer_top_batch = pyglet.graphics.Batch()


        # groups for rendering
        self.background_board_group = pyglet.graphics.Group(0)
        self.foreground_board_group = pyglet.graphics.Group(1)

        # background images : white, blue
        self.white_bg_image = pyglet.image.SolidColorImagePattern(color=(255,255,255,255)).create_image(width=self.img_pix, height=self.img_pix)
        self.blue_bg_image = pyglet.image.SolidColorImagePattern(color=(173,216,230,255)).create_image(width=self.img_pix, height=self.img_pix)

        # tanish tile uses color (204 150 77) 64x64 pixels
        #self.game_tile_image = pyglet.image.SolidColorImagePattern(color=(204, 150, 77, 255)).create_image(width=self.img_pix, height=self.img_pix)
        #self.game_tile_image = pyglet.image.load(self.png_path + "misc/tile.png")
        self.base_img = pyglet.image.load(self.png_path + "misc/tile.png")
        #self.game_tile_image.save(self.png_path + "misc/tile.png")

        # green cube uses color (18, 239, 0) 50x50 pixels
        self.gcube_image = pyglet.image.load(self.png_path + "misc/gcube.png")
        #self.gcube_image = pyglet.image.SolidColorImagePattern(color=(18, 239, 0, 255)).create_image(width=self.img_pix, height=self.img_pix)
        #self.gcube_image.save(self.png_path + "misc/gcube.png")

        # pink cube uses color (237, 13, 255) 34x34 pixels
        self.cube_image = pyglet.image.load(self.png_path + "misc/cube.png")
        #self.cube_image = pyglet.image.SolidColorImagePattern(color=(237, 13, 255, 255)).create_image(width=self.img_pix, height=self.img_pix)
        #self.cube_image.save(self.png_path + "misc/cube.png")
        #self.cube_image = pyglet.shapes.BorderedRectangle(0, 0, width=self.img_pix, height=self.img_pix, border=20, color=(237, 13, 255), border_color=(0, 0, 0))

        self.sprite_list = []
        sprite = pyglet.sprite.Sprite(self.base_img)
        self.sprite_list.append([self.base_img, sprite])
        for i in range(len(self.color_list)):
            image = pyglet.image.SolidColorImagePattern(color=self.color_list[i]).create_image(width=self.img_pix, height=self.img_pix)
            sprite = pyglet.sprite.Sprite(image)
            self.sprite_list.append([image, sprite])

        self.cube_sprites = []
        # put the gcube and cube someplace.
        # i may not need these eventually so not going to make this
        # a function for now...
        x_pos = 0
        y_pos = 0
        self.gcube = pyglet.sprite.Sprite( self.gcube_image, batch=self.pointer_bottom_batch, x = x_pos, y = y_pos)
        self.gcube.visible = True
        self.cube_sprites.append(self.gcube)
        self.cube = pyglet.sprite.Sprite( self.cube_image, batch=self.pointer_top_batch, x = x_pos, y = y_pos)
        self.cube.visible = False
        self.cube_sprites.append(self.cube)

        self.user_actions_allowed = True
        self.show_board = 0

        # if there is a game saved use it
        self.boards = []

        LoadGame (self)

        # did we load any boards or not
        if (len(self.boards) == 0):

            random.seed()
            self.do_random_board = True

            self.boards.append(Board(self, self.game_rows, self.game_cols, self.img_pix, self.img_pix, True, None, self.batch, self.background_board_group))
            self.boards.append(Board(self, self.game_rows, self.game_cols, self.img_pix, self.img_pix, False, None, self.over_batch, self.foreground_board_group))

        ResizeBoard (self)


    def on_draw(self):
        self.render()


    def on_close(self):
        print ("Exiting...")
        exit()


    def on_mouse_press(self, x, y, button, modifiers):

        # only do things when something else isn't happening
        if (self.user_actions_allowed == True):
            img_pix = self.img_pix
            x_win = x // img_pix
            x_rec = x_win * img_pix
            y_win = y // img_pix
            y_rec = y_win * img_pix
            win_pos = (y_win * self.window_cols) + x_win

            if button == mouse.LEFT:
                print("The LEFT mouse button was pressed.", x, x_rec, x_win, y, y_rec, y_win, win_pos)
                ActiveAreaLeftMouseClickAction(self, x, x_rec, y, y_rec, win_pos)
            elif button == mouse.MIDDLE:
                print("The MIDDLE mouse button was pressed.", x, x_rec, x_win, y, y_rec, y_win, win_pos)
                pass
            elif button == mouse.RIGHT:
                print("The RIGHT mouse button was pressed.", x, x_rec, x_win, y, y_rec, y_win, win_pos)
                ActiveAreaRightMouseClickAction(self, x, x_rec, y, y_rec, win_pos)


    def on_mouse_release(self, x, y, button, modifiers):
        #print ("The mouse was released")
        pass


    def on_mouse_motion(self, x, y, dx, dy):

        # don't do anything when something else is happening
        if (self.user_actions_allowed == False):
            return ()

        img_pix = self.img_pix
        x_win = x // img_pix
        x_rec = x_win * img_pix
        y_win = y // img_pix
        y_rec = y_win * img_pix
        win_pos = (y_win * self.window_cols) + x_win

        self.mouse_win_pos = win_pos
        ActiveAreaMouseMoveAction(self, x, x_rec, y, y_rec, win_pos)


    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        pass


    def on_mouse_leave(self, x, y):
        pass


    def on_mouse_enter(self, x, y):
        pass


    def on_key_press(self, symbol, modifiers):

        self.keys_held.append(symbol)
        if ((symbol == pyglet.window.key.ESCAPE) or (symbol == pyglet.window.key.Q)): # [ESC] or [Q]
            print ("The 'ESC' or 'Q' key was pressed.  Exiting Game...")
            exit()
        elif ((symbol == pyglet.window.key.F1) or
            (symbol == pyglet.window.key.QUESTION) or
            (symbol == pyglet.window.key.H)):
            ShowAbout (self)
            #print ("The 'F1', 'H', or '?' key was pressed ")
            pass
        elif symbol == pyglet.window.key.F2:
            print ("The 'F2' key was pressed, show board ", self.show_board)
            self.show_board = (self.show_board + 1) % 2

            if (self.show_board == 0):
                self.background_board_group.visible = False
                self.foreground_board_group.visible = True
                self.cube.visible = False
                self.gcube.visible = True
            elif (self.show_board == 1):
                self.background_board_group.visible = True
                self.foreground_board_group.visible = False
                self.cube.visible = True
                self.gcube.visible = False
            print ("The 'F2' key was pressed, show board changed to ", self.show_board)
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.F6)):
            print ("The 'F6' key was pressed")
            LoadGame (self)
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.F7)):
            print ("The 'F7' key was pressed")
            SaveGame (self)
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.F8)):
            print ("The 'F8' key was pressed")
            new_random_game (self)
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.F10)):
            print ("The 'F10' key was pressed")
            CheckBoard (self)
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.F11)):
            print ("The 'F11' key was pressed")
            DeleteSavedGame (self)
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.LEFT)):
            if self.game_cols > self.min_cols:
                self.game_rows = self.game_rows
                self.game_cols = self.game_cols - 1
                self.do_random_board = True
            print ("The 'LEFT' key was pressed")
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.RIGHT)):
            if self.game_cols < self.max_cols:
                self.game_rows = self.game_rows
                self.game_cols = self.game_cols + 1
                self.do_random_board = True
            print ("The 'RIGHT' key was pressed")
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.UP)):
            if self.game_rows < self.max_rows:
                self.game_rows = self.game_rows + 1
                self.game_cols = self.game_cols
                self.do_random_board = True
            print ("The 'UP' key was pressed")
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.DOWN)):
            if self.game_rows > self.min_rows:
                self.game_rows = self.game_rows - 1
                self.game_cols = self.game_cols
                self.do_random_board = True
            print ("The 'DOWN' key was pressed")
        else:
           pass


    def on_key_release(self, symbol, modifiers):
        try:
            self.keys_held.pop(self.keys_held.index(symbol))
            #print ("The key was released")
        except:
            pass


    def update(self, dt):
        pass


    def render(self):

        self.clear()

        self.batch.draw()
        self.over_batch.draw()
        self.fixed_batch.draw()
        self.fixed_board_batch.draw()
        self.pointer_bottom_batch.draw()
        self.pointer_middle_batch.draw()
        self.pointer_top_batch.draw()

        self.fps.draw()


def main():

    window = Window(width=1, height=1, caption="Npath", resizable=True, fullscreen=False, visible=False)

    pyglet.clock.schedule_interval(window.update, 1/60.0) # update at 60Hz
    pyglet.app.run()


if __name__ == "__main__":
    main()


