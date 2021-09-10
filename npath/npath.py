#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

import copy, os, random
from pathlib import Path

import pyglet
from pyglet.window import mouse
from pyglet.image import SolidColorImagePattern
from pyglet import clock


from active import ActiveAreaLeftMouseClickAction, ActiveAreaRightMouseClickAction, ActiveAreaMouseMoveAction
from board import Board
from button import SolidColorButtonImagePattern, SolidColorButtonImagePatternV00
from dialog import ChangeLayout, CheckBoard, DeleteSavedGame, LoadGame, SaveGame, ShowAbout
from version import GetVersion


def load_and_generate_or_resize_images (self):

    # this can be called more than once (when someone increases or
    # decreases img_pix).
    print ("Basic Tile and Image Size : ", str(self.img_pix) + " x " + str(self.img_pix) + " pixels")

    # colors
    color_list = [
        (  0,   0,   0, 255),  # black
        (255,   0,   0, 255),  # red
        (  0, 255,   0, 255),  # green
        (  0,   0, 255, 255),  # blue
        (128,   0, 128, 255),  # purple
        (255, 165,   0, 255),  # orange
        (255, 255,   0, 255),  # yellow
        (  0, 255, 255, 255),  # cyan
        (255,   0, 255, 255),  # fuchia
        (255, 255, 255, 255),  # white
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

    print("Length of color list : ", len(color_list))


    # tanish tile uses color (204 150 77) 64x64 pixels.  the two lines
    # commented out were ones used to create and save the initial image
    # and then i used gimp to put a border on it.
    #
    # instead of being limited to certain sized images it would be fun
    # to figure out how to do all of these as img_pix changes so not to
    # require all of these files be created...  but for now the sizes
    # have to be done manually.
    #
    #self.game_tile_image = pyglet.image.SolidColorImagePattern(color=(204, 150, 77, 255)).create_image(width=self.img_pix, height=self.img_pix)
    #self.game_tile_image.save(self.png_path + "misc/gen_tile.png")
    try:
        del self.base_image_tex
    except:
        pass

    f_name = str(self.png_path) + "misc/tile_" + str(self.img_pix) + ".png"
    #print("f_name : ", f_name)
    ft_name = "tile_" + str(self.img_pix) + ".png"
    #print("ft_name : ", ft_name)
    path = Path(f_name)
    if (path.is_file() == True):
        if (self.button_style != None):
            self.last_button_style = self.button_style
        self.button_style = None
        self.base_image_tex = pyglet.resource.Loader (pyglet.resource.path).texture (ft_name)
    else:
        if (self.button_style == None):
            self.button_style = self.last_button_style
        print ("Button Style : ", self.button_style)
        if (self.button_style == 0):
            self.base_image_tex = SolidColorButtonImagePattern (color=(204, 150, 77, 255), border_color=(0, 0, 0, 0)).create_image (width=self.img_pix, height=self.img_pix).get_texture ()
        elif (self.button_style == 1):
            self.base_image_tex = SolidColorButtonImagePattern (color=(204, 150, 77, 255), border_color=(204, 150, 77, 255)).create_image (width=self.img_pix, height=self.img_pix).get_texture ()
        elif (self.button_style == 2):
            self.base_image_tex = SolidColorButtonImagePatternV00 (color=(204, 150, 77, 255), border_color=(0, 0, 0, 0)).create_image (width=self.img_pix, height=self.img_pix).get_texture ()
        elif (self.button_style == 3):
            self.base_image_tex = SolidColorButtonImagePatternV00 (color=(204, 150, 77, 255), border_color=(204, 150, 77, 0)).create_image (width=self.img_pix, height=self.img_pix).get_texture ()

    # the first sprite make from the base_tile after that add 
    # all the images of colors from the above color_list
    try:
        self.image_list
    except:
        self.image_list = []
        self.image_list.append (self.base_image_tex)
        for i in range (len (color_list)):
            image_tex = pyglet.image.SolidColorImagePattern (color=color_list[i]).create_image (width=self.img_pix, height=self.img_pix).get_texture ()
            self.image_list.append (image_tex)
    else:
        # replace images in the list with different sized images
       self.image_list[0] = self.base_image_tex
       for i in range (len (color_list)):
           image_tex = pyglet.image.SolidColorImagePattern (color=color_list[i]).create_image (width=self.img_pix, height=self.img_pix).get_texture ()
           self.image_list[i+1] = image_tex

    print("Length of self.image_list : ", len(self.image_list), "  Base tile image is always image 0")

    # green cube uses color (18, 239, 0) 50x50 pixels (centered in 64x64)
    try:
        self.gcube_image
    except:
        self.gcube_image = pyglet.image.load(self.png_path + "misc/gcube.png")

        # useful things that i want to remember
        #self.gcube_image = pyglet.image.SolidColorImagePattern(color=(18, 239, 0, 255)).create_image(width=self.img_pix, height=self.img_pix)
        #self.gcube_image.save(self.png_path + "misc/gen_gcube.png")

    # pink cube uses color (237, 13, 255) 34x34 pixels (centered in 64x64)
    try:
        self.cube_image
    except:
        self.cube_image = pyglet.image.load(self.png_path + "misc/cube.png")

        # more useful things that i want to remember
        #self.cube_image = pyglet.image.SolidColorImagePattern(color=(237, 13, 255, 255)).create_image(width=self.img_pix, height=self.img_pix)
        #self.cube_image.save(self.png_path + "misc/gen_cube.png")
        #self.cube_image = pyglet.shapes.BorderedRectangle(0, 0, width=self.img_pix, height=self.img_pix, border=20, color=(237, 13, 255), border_color=(0, 0, 0))


class Window(pyglet.window.Window):


    def __init__ ( self, width, height, caption, resizable, fullscreen, visible, *args, **kwargs):


        super().__init__(width, height, caption, resizable, fullscreen, visible, *args, **kwargs)


        print("Pyglet version : ", pyglet.version)
        print("OpenGL version : ", self.context.get_info().get_version())
        print("Npath version  : ", GetVersion(), "\n")


        #   save game location and initial file
        # you can always save/load other names, 
        # this is just a suggestion...
        self.suggested_fn = "save.json"
        self.this_fn_to_open = self.suggested_fn
        self.this_fn_to_save = self.suggested_fn

        self.home = Path.home ()
        self.saved_dir = None

        # the path to the images
        self.png_path = os.path.dirname (__file__) + "/graphics/"
        print ("self.png_path : ", self.png_path)
        pyglet.resource.path = [".", "graphics/", "graphics/misc/"]
        pyglet.resource.reindex ()

        prog_name, prog_ext = os.path.splitext (os.path.basename (__file__))
        
        # i don't need this path for now but i'll leave this in just in case
        # someone else needs this for the future
        #self.settings_path = Path(pyglet.resource.get_settings_path (prog_name))
        #print ("self.settings_path : ", self.settings_path)
        if (pyglet.version.startswith("1.5") == True):
            self.data_path = Path(os.getenv("HOME") + "/.local/share/" + prog_name)
        else:
            self.data_path = Path(pyglet.resource.get_data_path (prog_name))
        print ("self.data_path : ", self.data_path)

        # these are the list of sizes, only some of these are bordered tiles 
        #   the too small ones (1, 2, 4) you can't see them anyways and
        #   the biggest one (1024) i'm not sure anyone would use that...
        self.pix_list = [1, 2, 3, 4, 8, 10, 16, 32, 50, 64, 96, 100, 128, 150, 192, 200, 256, 300, 512, 750, 1024]
        self.pix_index = 8
        self.img_pix = self.pix_list[self.pix_index]
        self.wiggle_room = self.img_pix // 2

        # any other value than in self.pix_list will work but the
        # initial screen will all be the flat images, you won't know
        # where the squares are at...  down to 1 pixel or as big as 
        # you'd like to try to see if your machine can handle it.
        # 1 pixel sized large games take a while to generate or change.


        # some limits and testing values

        self.min_rows = 1     # must be 1 or greater
        self.min_cols = 1     #

        self.max_rows = 300    # for temporary testing - i don't know how big
        self.max_cols = 300    #    the values i can put in here.


        # board size if no saved board exists (dimensions)
        self.game_rows = 3      # height
        self.game_cols = 5      # width

        # and some testing values
        #self.game_rows = 1    # height
        #self.game_cols = 1    # width
 
        # to fill the full screen in 1920 1080 with 64x64 pixel tiles
        #self.game_rows = 15   # height
        #self.game_cols = 30   # width


        # screens, sizes and locations
        #   some of these change as the board changes size
        self.top_display = pyglet.canvas.get_display ()
        self.top_screen = self.top_display.get_default_screen ()
        self.full_screen_width = self.top_screen.width
        self.full_screen_height = self.top_screen.height
        print ("Full Window Size :  ", self.full_screen_width, "x", self.full_screen_height, " pixels")
        self.windows_lst = self.top_display.get_windows ()
        self.wl0 = self.windows_lst[0]
        self.screen_width = self.windows_lst[0].width
        self.screen_height = self.windows_lst[0].height
        self.x, self.y = self.windows_lst[0].get_location ()
        print ("WL[0] Location\n  X Y       :  ", self.x, self.y, "\n  Size      :  ", self.screen_width, self.screen_height, " pixels\n  Rows Cols :  ", self.game_rows, self.game_cols, "\n")

        # other useful constants
        self.board_squares = self.game_rows * self.game_cols
        self.window_rows = self.game_rows
        self.window_cols = self.game_cols
        self.window_squares = self.window_rows * self.window_cols

        self.keys_held = []
        self.key = pyglet.window.key

        self.mouse_win_pos = 0
        self.user_mouse_resize = False
        self.user_mouse_check_insensitivity = 0
        self.user_mouse_check_level = 3
        self.user_mouse_action = pyglet.window.key.SPACE  # not doing anything


        # batches for rendering board layers
        self.under_batch = pyglet.graphics.Batch()
        self.over_batch = pyglet.graphics.Batch()

        # batches for rendering everything else
        self.pointer_bottom_batch = pyglet.graphics.Batch()
        self.pointer_middle_batch = pyglet.graphics.Batch()
        self.pointer_top_batch = pyglet.graphics.Batch()
        self.magnifier_bottom_batch = pyglet.graphics.Batch()
        self.magnifier_top_batch = pyglet.graphics.Batch()

        # groups for rendering
        if (pyglet.version.startswith("1.5") == True):
            self.background_board_group = pyglet.graphics.OrderedGroup(0)
            self.foreground_board_group = pyglet.graphics.OrderedGroup(1)
            self.magnifier_group = pyglet.graphics.OrderedGroup(2)
        else:
            self.background_board_group = pyglet.graphics.Group(0)
            self.foreground_board_group = pyglet.graphics.Group(1)
            self.magnifier_group = pyglet.graphics.Group(2)
        self.magnifier_group.visible = False

        self.button_style = None
        self.last_button_style = 0

        self.fps = pyglet.window.FPSDisplay (self)

        # these can change based upon size of img_pix
        load_and_generate_or_resize_images (self)

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

            self.boards.append(Board(self, self.game_rows, self.game_cols, self.img_pix, self.img_pix, False, None, self.over_batch, self.foreground_board_group))
            self.boards.append(Board(self, self.game_rows, self.game_cols, self.img_pix, self.img_pix, True, None, self.under_batch, self.background_board_group))

        self.window_resize (None)


    def boards_resize (self, key):

        # adjust the boards to fit
        if (key != None):
            for x in range (len (self.boards)):
                self.boards[x].board_resize (self, key)


    def window_resize (self, key):

        print ("\nwindow_resize")

        # ok, let's see...
        self.set_visible (True)

        # where are we now
        self.x, self.y = self.get_location ()
        self.screen_width, self.screen_height = self.get_size ()
        print ("  Loc Pre  X Y : ", self.x, self.y, "  W H : ", self.screen_width, self.screen_height)

        if (key == pyglet.window.key.LEFT):
            if (self.game_cols > self.min_cols):
                self.boards_resize (key)
                self.game_cols -= 1
            else:
                self.game_cols = self.min_cols
        elif (key == pyglet.window.key.RIGHT):
            if (self.game_cols < self.max_cols):
                self.boards_resize (key)
                self.game_cols += 1
            else:
                self.game_cols = self.max_cols
        elif (key == pyglet.window.key.UP):
            if (self.game_rows < self.max_rows):
                self.boards_resize (key)
                self.game_rows += 1
            else:
                self.game_rows = self.max_rows
        elif (key == pyglet.window.key.DOWN):
            if (self.game_rows > self.min_rows):
                self.boards_resize (key)
                self.game_rows -= 1
            else:
                self.game_rows = self.min_rows

        self.window_rows = self.game_rows
        self.window_cols = self.game_cols
        self.board_squares = self.game_rows * self.game_cols
        self.window_squares = self.window_rows * self.window_cols

        # adjust the main window size to fit
        self.screen_width = self.window_cols * self.img_pix
        self.screen_height = self.window_rows * self.img_pix

        self.x = (self.full_screen_width - self.screen_width) // 2
        self.y = (self.full_screen_height - self.screen_height) // 2
        print ("  Loc Post X Y : ", self.x, self.y, "  W H : ", self.screen_width, self.screen_height)

        self.set_size (self.screen_width, self.screen_height)
        self.set_location (self.x, self.y)
        print ("Resized WL[0] Location\n  X Y       :  ", self.x, self.y, "\n  Size      :  ", self.screen_width, self.screen_height, " pixels\n  Rows Cols :  ", self.game_rows, self.game_cols)

        # attempt to restore keyboard focus to the window
        self.activate ()


    def redraw (self):
        for x in range(len(self.boards)):
            self.boards[x].tile_height = self.img_pix
            self.boards[x].tile_width = self.img_pix
            self.boards[x].redraw (self.image_list)


    def new_random_game (self):

        print ("New Random Game")
        self.boards[1].bd_randomize (self.image_list)


    def on_draw (self):

        self.clear()

        self.under_batch.draw()
        self.over_batch.draw()
        self.pointer_bottom_batch.draw()
        self.pointer_middle_batch.draw()
        self.pointer_top_batch.draw()
        self.magnifier_bottom_batch.draw()
        self.magnifier_top_batch.draw()

        #self.fps.draw()


    def on_close (self):
        print ("Exiting...")
        exit()


    def on_mouse_press (self, x, y, button, modifiers):

        # only do things when something else isn't happening
        if (self.user_actions_allowed == True):
            #print ("on_mouse_press : ", x, y)
            img_pix = self.img_pix
            x_win = x // img_pix
            x_rec = x_win * img_pix
            y_win = y // img_pix
            y_rec = y_win * img_pix
            win_pos = (y_win * self.window_cols) + x_win

            if button == mouse.LEFT:
                #print("The LEFT mouse button was pressed.", x, x_rec, x_win, y, y_rec, y_win, win_pos)
                #ActiveAreaLeftMouseClickAction(self, x, x_rec, y, y_rec, win_pos)
                pass
            elif button == mouse.MIDDLE:
                #print("The MIDDLE mouse button was pressed.", x, x_rec, x_win, y, y_rec, y_win, win_pos)
                pass
            elif button == mouse.RIGHT:
                #print("The RIGHT mouse button was pressed.", x, x_rec, x_win, y, y_rec, y_win, win_pos)
                #ActiveAreaRightMouseClickAction(self, x, x_rec, y, y_rec, win_pos)
                pass


    def on_mouse_release (self, x, y, button, modifiers):

        # don't do anything when something else is happening
        if (self.user_actions_allowed == True):
            #print ("on_mouse_release : ", x, y)

            # if they were doing something clear that out
            if (self.user_mouse_action != pyglet.window.key.SPACE):
                self.user_mouse_action = pyglet.window.key.SPACE


    def on_mouse_motion (self, x, y, dx, dy):
        #print ("On_Mouse_Motion  X Y  dx dy :", x, y, dx, dy)
        pass


    def on_mouse_drag (self, x, y, dx, dy, buttons, modifiers):

        # don't do anything when something else is happening
        if (self.user_actions_allowed == False):
            return ()

        if (self.user_mouse_resize == True):
            #print ("On_Mouse_Drag  X Y  dx dy :", x, y, dx, dy)

            if (dx == 0) and (dy == 0):
                return

            if (self.user_mouse_check_insensitivity != self.user_mouse_check_level):
                self.user_mouse_check_insensitivity += 1
                return
            else:
                self.user_mouse_check_insensitivity = 0


            if (self.user_mouse_action == pyglet.window.key.SPACE):

                # divide the screen into halfs and interpret drag
                # direction to set the user_mouse_action
                #
                # start with the left
                if (x in range (0, self.screen_width // 2)):
                    if ((dx < 0) and (dy == 0)):
                        #print ("L Make Fatter")
                        self.user_mouse_action = pyglet.window.key.RIGHT
                    elif ((dx > 0) and (dy == 0)):
                        #print ("L Make Skinnier")
                        self.user_mouse_action = pyglet.window.key.LEFT

                # then the right
                elif (x in range (self.screen_width // 2, self.screen_width)):
                    if ((dx < 0) and (dy == 0)):
                        #print ("R Make Skinnier")
                        self.user_mouse_action = pyglet.window.key.LEFT
                    elif ((dx > 0) and (dy == 0)):
                        #print ("R Make Fatter")
                        self.user_mouse_action = pyglet.window.key.RIGHT

                # now the bottom
                if (y in range (0, self.screen_height // 2)):
                    if ((dx == 0) and (dy < 0)):
                        #print ("B Make Taller")
                        self.user_mouse_action = pyglet.window.key.UP
                    elif ((dx == 0) and (dy > 0)):
                        #print ("B Make Shorter")
                        self.user_mouse_action = pyglet.window.key.DOWN

                # then the top
                elif (y in range (self.screen_height // 2, self.screen_height)):
                    if ((dx == 0) and (dy < 0)):
                        #print ("T Make Shorter")
                        self.user_mouse_action = pyglet.window.key.DOWN
                    elif ((dx == 0) and (dy > 0)):
                        #print ("T Make Taller")
                        self.user_mouse_action = pyglet.window.key.UP

            # an action is underway, keep doing it as long as
            # the user keeps the mouse pressed or the max or min
            # sizes are reached
            else:
                self.window_resize (self.user_mouse_action)


    def mouse_leave (self, x, y):
        pass


    def on_mouse_enter (self, x, y):
        pass


    def on_key_press (self, symbol, modifiers):

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
                self.background_board_group.visible = True
                self.foreground_board_group.visible = True
                self.cube.visible = False
                self.gcube.visible = True
                self.user_actions_allowed = True
            elif (self.show_board == 1):
                self.background_board_group.visible = True
                self.foreground_board_group.visible = False
                self.cube.visible = True
                self.gcube.visible = False
                self.user_actions_allowed = True
            print ("The 'F2' key was pressed, show board changed to ", self.show_board)
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.F4)):
            self.user_mouse_resize = not (self.user_mouse_resize)
            print ("The 'F4' key was pressed, user_mouse_resize ", self.user_mouse_resize)
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.F6)):
            print ("The 'F6' key was pressed")
            LoadGame (self)
            load_and_generate_or_resize_images (self)
            self.redraw ()
            self.window_resize (None)
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.F7)):
            print ("The 'F7' key was pressed")
            SaveGame (self)
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.F8)):
            print ("The 'F8' key was pressed")
            self.new_random_game ()
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.F9)):
            print ("The 'F9' key was pressed")
            if (self.magnifier_group.visible == False):
                if (self.button_style == None):
                    self.button_style = self.last_button_style
                self.background_board_group.visible = False
                self.foreground_board_group.visible = False
                self.cube.visible = False
                self.gcube.visible = False
                self.user_actions_allowed = True
                while (self.game_cols > 1):
                    self.window_resize (pyglet.window.key.LEFT)
                while (self.game_rows > 1):
                    self.window_resize (pyglet.window.key.DOWN)
                self.pix_index = len(self.pix_list) - 1
                self.img_pix = self.pix_list[self.pix_index]
                load_and_generate_or_resize_images (self)
                self.background_board_group.visible = True
                self.foreground_board_group.visible = True
                self.redraw ()
                self.window_resize (None)
                self.mag_sprite_bg = pyglet.sprite.Sprite(self.boards[1].tiles[0].spr.image.get_region(0,0,64,64),batch=self.magnifier_bottom_batch,group=self.magnifier_group)
                self.mag_sprite_bg.update(scale=8, x=256, y=256)
                self.mag_sprite_ll = pyglet.sprite.Sprite(self.boards[0].tiles[0].spr.image.get_region(0,0,32,32),batch=self.magnifier_top_batch,group=self.magnifier_group)
                self.mag_sprite_ll.update(scale=8, x=256, y=256)
                self.mag_sprite_lr = pyglet.sprite.Sprite(self.boards[0].tiles[0].spr.image.get_region(1024-32,0,32,32),batch=self.magnifier_top_batch,group=self.magnifier_group)
                self.mag_sprite_lr.update(scale=8, x=512, y=256)
                self.mag_sprite_ul = pyglet.sprite.Sprite(self.boards[0].tiles[0].spr.image.get_region(0,1024-32,32,32),batch=self.magnifier_top_batch,group=self.magnifier_group)
                self.mag_sprite_ul.update(scale=8, x=256, y=512)
                self.mag_sprite_ur = pyglet.sprite.Sprite(self.boards[0].tiles[0].spr.image.get_region(1024-32,1024-32,32,32),batch=self.magnifier_top_batch,group=self.magnifier_group)
                self.mag_sprite_ur.update(scale=8, x=512, y=512)
                self.magnifier_group.visible = True
            else:
                self.magnifier_group.visible = False
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.F10)):
            print ("The 'F10' key was pressed")
            CheckBoard (self)
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.F11)):
            print ("The 'F11' key was pressed")
            DeleteSavedGame (self)
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.LEFT)):
            self.window_resize (pyglet.window.key.LEFT)
            print ("The 'LEFT' key was pressed")
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.RIGHT)):
            self.window_resize (pyglet.window.key.RIGHT)
            print ("The 'RIGHT' key was pressed")
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.UP)):
            self.window_resize (pyglet.window.key.UP)
            print ("The 'UP' key was pressed")
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.DOWN)):
            self.window_resize (pyglet.window.key.DOWN)
            print ("The 'DOWN' key was pressed")
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.NUM_ADD)):
            print ("The 'NUM_ADD' key was pressed")
            if (self.pix_index < len(self.pix_list)-1):
                self.pix_index += 1
                self.img_pix = self.pix_list[self.pix_index]
                load_and_generate_or_resize_images (self)
                self.redraw ()
                self.window_resize (None)
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.NUM_SUBTRACT)):
            print ("The 'NUM_SUBTRACT' key was pressed")
            if (self.pix_index > 0):
                self.pix_index -= 1
                self.img_pix = self.pix_list[self.pix_index]
                load_and_generate_or_resize_images (self)
                self.redraw ()
                self.window_resize (None)
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.P)):
            print (self.boards[self.show_board])
        elif ((self.show_board in [0,1]) and (symbol == pyglet.window.key.B)):
            if (self.button_style != None):
                self.button_style = (self.button_style + 1) % 4
                self.last_button_style = self.button_style
                load_and_generate_or_resize_images (self)
                self.redraw ()
                self.window_resize (None)
            else:
                print ("The Button Style is from a loaded image")
        else:
           pass


    def on_key_release (self, symbol, modifiers):
        try:
            self.keys_held.pop (self.keys_held.index(symbol))
            #print ("The key was released")
        except:
            pass


    def update (self, dt):
        pass


def main ():

    window = Window (width=1, height=1, caption="Npath", resizable=True, fullscreen=False, visible=False)

    pyglet.clock.schedule_interval (window.update, 1/60.0) # update at 60Hz
    pyglet.app.run ()


if __name__ == "__main__":
    main()


