Coin Collector
==============

Libraries used
--------------
- Pygame Zero (`pgzrun`) provides the game window, input, drawing, actors,
  audio, and game loop.
- Pygame's `Rect` class is used for the arena and enemy movement areas. Pygame
  is installed as a dependency of Pygame Zero.
- Python's standard-library `math` module is used to normalize diagonal
  movement.

The `random` module is not used by this version of the project.

Run the project
---------------
1. Install Python 3.13 and make sure the Python launcher (`py`) can find it.
   Pygame Zero depends on Pygame; use Python 3.13 for this project because
   the Python 3.14 install in this environment could not build its Pygame
   dependency.
2. From this project's directory, install Pygame Zero:

       py -3.13 -m pip install pgzero

3. Start the game from the project directory:

       py -3.13 .\python-game\game.py

Keep the `images`, `music`, and `sounds` folders beside `game.py` inside the
`python-game` folder. Pygame Zero loads the game's artwork and audio from those
folders.
