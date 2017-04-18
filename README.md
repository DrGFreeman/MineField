# MineField
A game for the Minecraft Raspberry Pi edition.

By Julien de la Bruère-Terreault (drgfreeman@tuta.io)

# Summary
_MineField_ is a game programmed in Python for [Minecraft Pi edition](https://www.raspberrypi.org/learning/getting-started-with-minecraft-pi/) making use of
[physical computing](https://www.raspberrypi.org/learning/physical-computing-with-python/)
to control LEDs and a buzzer.

The player must find and destroy a [block of gold](http://minecraft.gamepedia.com/Block_of_Gold) then return to its starting point marked by a [glowing obsidian block](http://minecraft.gamepedia.com/Glowing_Obsidian).

Simple? Not so much!!!

The issue is that the Minecraft world is strewn with invisible land mines that the player must avoid to stay alive. To help him or her, the player is equipped with a mine detector indicating the distance to the nearest mine. The mine detector consists of four LEDs that light depending on the distance to the nearest mine, as well as a buzzer that buzzes an increasing number of beeps as the player gets closer to a mine. With the help of the mine detector, the player must navigate around the mines to find the block of gold and return to the starting point.

Try it out and _have a blast_!

# Screenshots

![Game start](/doc/img/start.png)<br>*Game start instructions. Note the red glowing obsidian block. The player will need to return to this block after having destroyed the block of gold.*

![Block of gold](/doc/img/gold.png)<br>*The block of gold to be found and destroyed.*

![Objective reached](/doc/img/objReached.png)<br>*Objective reached, now safely return to the starting point.*

![Succeeded](/doc/img/succeeded.png)<br>*Destroy the glowing obsidian block at the start position to complete the mission.*

![Oops!](/doc/img/boom.png)<br>*Oops! Things do not always go according to plan...*

# Installing the game

Minecraft Pi edition is installed by default on the Raspberry Pi Raspbian distribution. There is therefore no need to install it.

To install the _MineField_ game, open a terminal on the Raspberry Pi and clone the game's [GitHub repository](https://github.com/DrGFreeman/MineField) with the following command:

`git clone https://github.com/DrGFreeman/MineField.git`

# Playing the game

Prior launching the game, launch Minecraft Pi edition on the Raspbery Pi and enter the world of your choice.  See [Getting Started with Minecraft Pi](https://www.raspberrypi.org/learning/getting-started-with-minecraft-pi/worksheet/) in the [Raspberry Pi Learning Resources](https://www.raspberrypi.org/resources/) for an introduction to Minecraft Pi edition.

Beware, mine explosions may create craters or damage constructions in the selected world. If you want to avoid any damage to your worlds, create a new world to play this game.

Hit the _TAB_ key to exit the Minecraft window.

To launch the game, open a terminal on the Raspbery Pi. Change to the MineField directory:

`cd MineField`

Launch the `minefield.py` script using Python 3:

`python3 minefield.py`

Double click in the Minecraft window to start playing.

To launch a new game, hit the _TAB_ key to exit the Minecraft window and relaunch the script in the terminal.

# Making the mine detector
The mine detector has two indication methods, a distance scale made of four [LEDs](https://www.raspberrypi.org/learning/physical-computing-with-python/worksheet/) and an [active buzzer](https://www.raspberrypi.org/learning/physical-computing-with-python/buzzer/) emitting a number of beeps equal to the number of LEDs lit.

The connections are as per the circuit below. The positive (long) legs of the LEDs as well as the active buzzer positive pin are connected to the Raspberry Pi GPIO pins indicated in the table below. The negative (short) legs of the LEDs are connected to ground through 220 ohm resistors (or any value above 50 ohm). The buzzer ground pin is connected directly to ground. If using a breadboard as shown, the breadboard ground must be connected to one of the Raspberry Pi ground pins.

Device | GPIO pin
-------|----------
Blue LED | 17
Green LED | 27
Yellow LED | 22
Red LED | 16
Buzzer | 4

![mine detector circuit](/doc/img/mineDetector_700px.png)

# Notes

* The game is designed to work with Python 3.
* The game can be played without the buzzer _or_ LEDs. This may make it more difficult to avoid mines.
* The game difficulty can be adjusted by changing the parameters below in the minefield.py file.

    ```python
    ########################################
    ### Game settings
    # Adjust these settings to control game difficulty level

    # Distance thresholds for mine detector LEDs and buzzer
    distBlue = 16
    distGreen = 8
    distYellow = 5
    distRed = 3

    # Distance threshold for mine explosion
    distMineTrigger = 1 # The mine explodes if the player is within this distance

    # Number of mines
    nbMines = 200

    # Extent of mine coverage around player (+/-)
    extentMines = 100

    # Distance to goal
    goalDist = 40
    ```

# Version history
1.0.0 (2017-04-16): Initial documented release
