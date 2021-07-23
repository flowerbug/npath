# General Information

  This is a project to take an old game that I converted to python, pyglet and gtk3 and change it into a more general framework for a variable sized grid.  Since all of the licensed old copyrighted materials will be removed eventually I will just point people to the old version that includes all the licenses for the old artwork.

  That old version is at https://www.github.com/flowerbug/ngfp which is based upon a game called gfpoken.

  As usual this is mainly something I'm doing to improve my python programming and to learn more about pyglet.

  If you go back in versions to checkout npath-v0.0.0 you will see it is a somewhat edited version of ngfp which has been changed only to change the name and some module imports.

  Version 0.0.1 tests how low the minimum row and column sizes work and as it turns out the game still works at 0 rows and columns even if it doesn't do anything interesting.  A 1 row by 1 column game is playable but silly and some of the menus on the right are chopped off.  The minimum playable simple game with fully visible menus is 6 rows and 1 column.  This is only temporary as the menu and widget piles are coming out.

  Version 0.1.0 is not a playable game.  It runs and doesn't crash but is merely being used to get ready for the more general framework.  Removing the control and widget menus to the right.  Displaying the random board and guess board will still work.

  Version 0.2.0 is still not a playable game.  It runs and the dialogs have been replaced by function keys.  So to see the whole list press 'F1', 'H' or '?'.

  Version 0.3.0 is still not a playable game.  Added arrow keys being able to resize the window between the configured max and min sizes for columns and rows.  This is not yet working quite right for centering and it should instead be based upon the maximum size of the window dimensions instead of fixed numbers in the config.  Version 0.3.1 is just a minor update to this README and the dialog for the help adding the arrow keys.  Version 0.3.2 is a minor bug fix version plus I bumped the config max limits to 50 for some testing.  Version 0.3.3 prints out window location and size.  Version 0.3.4 fixes my mistake.  Version 0.3.5 a few code cleanups.

  Version 0.4.0 is still not playable as a game.  I started to remove the previous images which are used to play the game this framework is taken from.  Version 0.4.1 updates this README.


# The next versions will be aiming towards

  Removing the artwork and replacing it by colors so that nothing will be based upon fixed sized images, which should allow us to get down to a pixel sized cell in the grid if we want.

  The logic of the game is changed to turn it into something that I've not figured out yet.

  Reducing the number of batches to one and using groups instead.
