# General Information

  This is a project to take an old game that I converted from C to python, pyglet and gtk3 and change it into a more general framework for a variable sized grid.  I've removed the previously licensed artwork and gtk so that this is entirely now under just the Apache license.  I've also been simplifying the code and removing extra things that aren't really needed.

  As usual this is mainly something I'm doing to improve my python programming and to learn more about pyglet.


# Versions Along the Way (in reverse order)

  Version 0.7.0 is a lot more simplified.  I've combined files, made some classes and methods, gotten rid of borders and the config file.  Many things still don't work yet (like the save and load game functions).  Version 0.7.1 removes the complication of having another layer of defaults.  Version 0.7.2 Save and Load work along with the initial load of a saved game.  Version 0.7.3 New Random Game and Check Game work.

  Version 0.6.0 is one step further of simplification.  There is no big need for a configuration file for the game.  Save the board sizes and border flag with the board itself.  If there isn't a board saved to start with when the game starts use the built in defaults.

  Version 0.5.0 makes the border and the white active border squares optional.  F12 toggles between views with and without borders.  Saving and Loading boards now include the borders flag as also does the configuration file when it is saved.  Version 0.5.1 continues working on fixing bugs.  This is not complete yet, so some bugs remain and I've decided I'm not going to completely debug this version because I plan on redoing more of the board drawing and parameters and such in a more object oriented fashion.  This is a lot more complicated than it needs to be.
  Version 0.4.0 is still not playable as a game.  I started to remove the previous images which are used to play the game this framework is taken from.  Version 0.4.1 updates this README.  Version 0.4.2 removes the old images and code that aren't used by anything (only cube and gcube are left).  Version 0.4.3 replaces cube and gcube so now all previous images are gone so everything now can go under the Apache License.

  Version 0.3.0 is still not a playable game.  Added arrow keys being able to resize the window between the configured max and min sizes for columns and rows.  This is not yet working quite right for centering and it should instead be based upon the maximum size of the window dimensions instead of fixed numbers in the config.  Version 0.3.1 is just a minor update to this README and the dialog for the help adding the arrow keys.  Version 0.3.2 is a minor bug fix version plus I bumped the config max limits to 50 for some testing.  Version 0.3.3 prints out window location and size.  Version 0.3.4 fixes my mistake.  Version 0.3.5 a few code cleanups.

  Version 0.2.0 is still not a playable game.  It runs and the dialogs have been replaced by function keys.  So to see the whole list press 'F1', 'H' or '?'.

  Version 0.1.0 is not a playable game.  It runs and doesn't crash but is merely being used to get ready for the more general framework.  Removing the control and widget menus to the right.  Displaying the random board and guess board will still work.

  Version 0.0.1 tests how low the minimum row and column sizes work and as it turns out the game still works at 0 rows and columns even if it doesn't do anything interesting.  A 1 row by 1 column game is playable but silly and some of the menus on the right are chopped off.  The minimum playable simple game with fully visible menus is 6 rows and 1 column.  This is only temporary as the menu and widget piles are coming out.


# The next versions will be aiming towards

  More OOP concepts.

  Resizing tiles.

  The logic of the game is changed to turn it into something that I've not figured out yet.

  Reducing the number of batches to one and using groups instead.
