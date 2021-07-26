#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright (c) Flowerbug <flowerbug@anthive.com>

import pyglet
from pyglet.window import mouse
from pyglet import clock

import config as cfg

from active import ActiveAreaLeftMouseClickAction, ActiveAreaRightMouseClickAction, ActiveAreaMouseMoveAction
from board import DrawBoard, RestartGame, ClearAndResizeBoard
from dialog import ChangeLayout, CheckBoard, CleanUpConfigAndSavedGame, LoadConfigOrUseCurrent, LoadSavedGameFromFile, NewRandomGame, RestoreConfigDefaults, SaveConfigToFile, SaveGameToFile, ShowAbout
from my_init import MyInitStuff
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

        self.set_visible(False)

        print("Pyglet version : ", pyglet.version)
        print("Npath version  : ", GetVersion())

        MyInitStuff (self)


    def on_draw(self):
        self.render()


    def on_close(self):
        exit()


    def on_mouse_press(self, x, y, button, modifiers):

        # only do things when something else isn't happening
        if (cfg.no_user_actions == False):
            img_pix = cfg.img_pix
            x_win = x // img_pix
            x_rec = x_win * img_pix
            y_win = y // img_pix
            y_rec = y_win * img_pix
            win_pos = (y_win * self.window_cols) + x_win

            if button == mouse.LEFT:
#                print("The LEFT mouse button was pressed.", x, x_rec, x_win, y, y_rec, y_win, win_pos)
                ActiveAreaLeftMouseClickAction(self, x, x_rec, y, y_rec, win_pos)
            elif button == mouse.MIDDLE:
#                print("The MIDDLE mouse button was pressed.", x, x_rec, x_win, y, y_rec, y_win, win_pos)
                pass
            elif button == mouse.RIGHT:
#                print("The RIGHT mouse button was pressed.", x, x_rec, x_win, y, y_rec, y_win, win_pos)
                ActiveAreaRightMouseClickAction(self, x, x_rec, y, y_rec, win_pos)


    def on_mouse_release(self, x, y, button, modifiers):
#        print ("The mouse was released")
        pass


    def on_mouse_motion(self, x, y, dx, dy):

        # don't do anything when something else is happening
        if (cfg.no_user_actions == True):
            return ()

        img_pix = cfg.img_pix
        x_win = x // img_pix
        x_rec = x_win * img_pix
        y_win = y // img_pix
        y_rec = y_win * img_pix
        win_pos = (y_win * self.window_cols) + x_win

        if (win_pos in self.guess_active_squares):
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
#            print ("The 'ESC' or 'Q' key was pressed")
            exit()
        elif ((symbol == pyglet.window.key.F1) or
            (symbol == pyglet.window.key.QUESTION) or
            (symbol == pyglet.window.key.H)):
            ShowAbout (self)
#            print ("The 'F1', 'H', or '?' key was pressed ")
            pass
        elif symbol == pyglet.window.key.F2:
#            print ("The 'F2' key was pressed, show board ", cfg.show_board)
            # after the initial showing of the background we
            # don't ever need to see the background again so 
            # only toggle between the game board and the guess 
            # board (0 or 1)...
            cfg.show_board = (cfg.show_board + 1) % 2

            if (cfg.show_board == 0):
                self.cube.visible = True
                self.gcube.visible = False
            elif (cfg.show_board == 1):
                self.cube.visible = False
                self.gcube.visible = True
#            print ("The 'F2' key was pressed, show board changed to ", cfg.show_board)
        elif ((cfg.show_board == 1) and (symbol == pyglet.window.key.F3)):
            print ("The 'F3' key was pressed")
            RestoreConfigDefaults()
        elif ((cfg.show_board == 1) and (symbol == pyglet.window.key.F4)):
            print ("The 'F4' key was pressed")
            LoadConfigOrUseCurrent()
        elif ((cfg.show_board == 1) and (symbol == pyglet.window.key.F5)):
            print ("The 'F5' key was pressed")
            SaveConfigToFile()
        elif ((cfg.show_board == 1) and (symbol == pyglet.window.key.F6)):
            print ("The 'F6' key was pressed")
            LoadSavedGameFromFile(self)
        elif ((cfg.show_board == 1) and (symbol == pyglet.window.key.F7)):
            print ("The 'F7' key was pressed")
            SaveGameToFile(self)
        elif ((cfg.show_board == 1) and (symbol == pyglet.window.key.F8)):
            print ("The 'F8' key was pressed")
            NewRandomGame(self)
        elif ((cfg.show_board == 1) and (symbol == pyglet.window.key.F9)):
            print ("The 'F9' key was pressed")
            RestartGame(self)
        elif ((cfg.show_board == 1) and (symbol == pyglet.window.key.F10)):
            print ("The 'F10' key was pressed")
            CheckBoard(self)
        elif ((cfg.show_board == 1) and (symbol == pyglet.window.key.F11)):
            print ("The 'F11' key was pressed")
            CleanUpConfigAndSavedGame()
        elif ((cfg.show_board == 1) and (symbol == pyglet.window.key.F12)):
            print ("The 'F12' key was pressed")
            ChangeLayout(self)
        elif ((cfg.show_board == 1) and (symbol == pyglet.window.key.LEFT)):
            if cfg.game_cols > cfg.min_cols:
                cfg.game_cols = cfg.game_cols - 1
                cfg.game_rows = cfg.game_rows
                cfg.show_board = 2  # reinitialize sprites and lists
                cfg.do_random_board = True
            print ("The 'LEFT' key was pressed")
        elif ((cfg.show_board == 1) and (symbol == pyglet.window.key.RIGHT)):
            if cfg.game_cols < cfg.max_cols:
                cfg.game_cols = cfg.game_cols + 1
                cfg.game_rows = cfg.game_rows
                cfg.show_board = 2  # reinitialize sprites and lists
                cfg.do_random_board = True
            print ("The 'RIGHT' key was pressed")
        elif ((cfg.show_board == 1) and (symbol == pyglet.window.key.UP)):
            if cfg.game_rows < cfg.max_rows:
                cfg.game_rows = cfg.game_rows + 1
                cfg.game_cols = cfg.game_cols
                cfg.show_board = 2  # reinitialize sprites and lists
                cfg.do_random_board = True
            print ("The 'UP' key was pressed")
        elif ((cfg.show_board == 1) and (symbol == pyglet.window.key.DOWN)):
            if cfg.game_rows > cfg.min_rows:
                cfg.game_rows = cfg.game_rows - 1
                cfg.game_cols = cfg.game_cols
                cfg.show_board = 2  # reinitialize sprites and lists
                cfg.do_random_board = True
            print ("The 'DOWN' key was pressed")
        else:
           pass


    def on_key_release(self, symbol, modifiers):
        try:
            self.keys_held.pop(self.keys_held.index(symbol))
#            print ("The key was released")
        except:
            pass


    def update(self, dt):
        pass


    def render(self):

        self.clear()

        DrawBoard (self)

        self.fixed_batch.draw()
        self.fixed_board_batch.draw()
        self.variable_board_batch.draw()
        self.variable_guess_batch.draw()
        self.pointer_bottom_batch.draw()
        self.pointer_top_batch.draw()

#        self.fps.draw()


def main():
    window = Window(width=cfg.img_pix*(cfg.game_cols+cfg.adj_size), height=cfg.img_pix*(cfg.game_rows+cfg.adj_size), caption="Npath", resizable=True, fullscreen=False, visible=False)
    pyglet.clock.schedule_interval(window.update, 1/120.0) # update at 60Hz
    pyglet.app.run()


if __name__ == "__main__":
    main()


