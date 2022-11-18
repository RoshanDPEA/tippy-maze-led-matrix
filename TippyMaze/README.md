# Tippy Maze

Software package to support the Tippy Maze project.
Additional documentation for this project can be found [here.](https://dpengineering.github.io/TippyMaze/)

## Current Status
This branch doesn't support the coin acceptor. There are issues when interfacing with the coin acceptor over serial as well as I2C for the 
lidar sensors. This may be fixed if the code is optimized.

## Use
Install the TippyMaze python module by running ```pip3 install -e .``` from within the repositories directory, this will install all (except pygame)
dependencies needed to run the project.

All aspects of hardware control have been packaged into their own classes to make hardware interaction as seamless as possible.

### Button Combos
There are certain buttons that can be pressed at the same time to have the project perform certain actions.

### Homing the table
The table can be homed at any point by pressing the trigger button and button "4".

### Require money
The project can be forced to require money before allowing gameplay by pressing the trigger and button "5".

### Reset the Game
The game can be reset where the table is homed, and a new gumball is released by pressing buttons labeled "8" and "9"

## Known Bugs
Currently when listing ```pygame``` as a requirement in setup.py the installation fails.
However this is easily fixed by running the command ```pip install pygame```.

Additionally, when listing ```busio``` as a requirement in setup.py the installation fails. However there doesn't seem to be
an issue not listing it as a requirement.