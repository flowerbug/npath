# General Information

  This is a project to take an old game that I converted to python, pyglet and gtk3 and change it into a more general framework for a variable sized grid.  Since all of the licensed old copyrighted materials will be removed eventually I will just point people to the old version that includes all the licenses for the old artwork.

  That old version is at https://www.github.com/flowerbug/ngfp which is based upon a game called gfpoken.

  As usual this is mainly something I'm doing to improve my python programming and to learn more about pyglet.

  If you go back in versions to checkout npath-v0.0.0 you will see it is a somewhat edited version of ngfp which has been changed only to change the name and some module imports.

  The next versions will be aiming towards:

    - removing the control menu and replacing those by keyboard commands.
      - all the dialogs get coverted or changed.

    - Removing the artwork and replacing it by colors so that nothing will be
      based upon fixed sized images, which should allow us to get down to a
      pixel sized cell in the grid if we want.

    - The logic of the game is removed to turn it into a simple matching 
      guessing game of colors.

    - Reducing the number of batches to one and using groups instead.
