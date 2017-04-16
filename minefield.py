# -*- coding: utf-8 -*-

# minefield.py
# Source: https://github.com/DrGFreeman/MineField
#
# MIT License
#
# Copyright (c) 2017 Julien de la Bruere-Terreault <drgfreeman@tuta.io>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

################################################################################
#
# MineField game for Raspbery Pi Minecraft edition.
#
# See README on GitHub repository for instructions:
# https://github.com/DrGFreeman/MineField/blob/master/README.md
#
################################################################################

import random
import time
import math

from mcpi.minecraft import Minecraft
from mcpi import block

from minedetector import MineDetector
from pt3d import Pt3D

########################################
### Functions

def clean():
    """Cleans the game blocks in case of interruption."""

    # set base and goal blocks to air
    mc.setBlock(base.x, base.y, base.z, block.AIR)
    mc.setBlock(goal.x, goal.y, goal.z, block.AIR)

def explosion(dim):
    """Create an explosion effect at the player position."""
    # get the player position
    p = mc.player.getTilePos()

    # set explosion dimensions
    d3 = dim
    d2 = d3 - 1
    d1 = d2 - 1

    # create a hole at the player position
    mc.setBlocks(p.x - d2, p.y - d1, p.z - d1, p.x + d2, p.y + d1, p.z + d1,
                 block.AIR)
    mc.setBlocks(p.x - d1, p.y - d1, p.z - d2, p.x + d1, p.y + d1, p.z + d2,
                 block.AIR)
    mc.setBlocks(p.x - d1, p.y - d2, p.z - d1, p.x + d1, p.y + d2, p.z + d1,
                 block.AIR)

    # create falling gravel and sand blocks above player.
    for i in range(-d3, d3):
        for j in range(-d3, d3):
            rand1 = random.randint(0, 4)
            rand2 = random.randint(0, 1)
            if rand1 > 0:
                if rand2 > 0:
                    mc.setBlock(p.x + i, p.y + d3, p.z + j, block.GRAVEL)
                else:
                    mc.setBlock(p.x + i, p.y + d3, p.z + j, block.SAND)

def popMines(mines, point, distance):
    """Removes mines located within a specidfied distance around a point from
    the mines list.
    """
    # list of the indexes of mines in proximity of the point (initially empty)
    minesProx = []
    
    # for all mines,
    for i in range(len(mines)):
        
         # calculate distance to mine
        distMine = point.distAxes(mines[i], 5)
        
        # if mine is within specified distance
        if distMine <= distance:
            # add mine index to proximity list
            minesProx.append(i)
            
    # if there are mines in the proximity list
    if len(minesProx) > 0:
        # for all mine indexes in proximity list
        for i in minesProx:
            # remove mine from mines list
            mines.pop(i)
            
    # print number of mines eliminated
    print("   ", len(minesProx), " Mines eliminated.")
    # return mines list
    return mines

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

########################################
### Game preparation

# Initialisation of the mine detector
mineDetector = MineDetector(distBlue, distGreen, distYellow, distRed)

# Connection to Minecraft Pi
mc = Minecraft.create()

## Random definition of the base location
print("Defining the base location")

# State variable defining whether the base block has been successfully defined
blockBaseOK = False

# Try base block positions until an acceptable position is found
while not blockBaseOK:

    # define a random point (Pt3D type) within +/- 35 blocks of world origin
    base = Pt3D(random.randint(-35, 35), 0, random.randint(-35, 35))

    # get world height at base position
    base.y = mc.getHeight(base.x, base.z)

    # get the block type under base position
    blockBaseType = mc.getBlock(base.x, base.y - 1, base.z)

    # check that block type not is water, lava or a tree
    if not blockBaseType in [8, 9, 10, 11, 18]:
        # base position is acceptable
        blockBaseOK = True

print("   Base position defined successfully.")

## Random generation of mines

print("Generating mines")

# List of mines (Pt3D objects, initially empty)
mines = []

# Do for each mine
for mine in range(nbMines):
    # create Pt3D type object at random location
    # and append it to the mines list.
    mines.append(Pt3D(random.randint(-extentMines, extentMines) + base.x, -64,
                 random.randint(-extentMines, extentMines) + base.z))

# Check and remove mines within trigger distance of base location
print("Verifying mines at start position")
mines = popMines(mines, base, distMineTrigger + 1)

## Define goal position (position relative to base location)

print("Défining the goal location")

# State variable defining whether the goal block has been successfully defined
blockGoalOK = False

# Try goal block positions until an acceptable position is found
while not blockGoalOK:

    # set the azimut to the goal randomly between -180 and 180 degrees
    goalAzimut = random.uniform(-math.pi, math.pi)

    # define a point (Pt3D type) at goal distance and goal azimut from base
    goal = Pt3D(goalDist * math.cos(goalAzimut) + base.x, 0,
                goalDist * math.sin(goalAzimut) + base.z)

    # get world height at goal position
    goal.y = mc.getHeight(goal.x, goal.z)

    # get the block type under goal position
    blockGoalType = mc.getBlock(goal.x, goal.y - 1, goal.z)

    # check that block type not is water, lava or a tree
    if not blockGoalType in [8, 9, 10, 11, 18]:
        # goal position is acceptable
        blockGoalOK = True

print("   Goal position defined successfully")

# Check and remove mines within trigger distance of base location
print("Verifying mines at goal position")
mines = popMines(mines, goal, distMineTrigger + 1)

# Create a glowing obsidian block at base position
mc.setBlock(base.x, base.y, base.z, block.GLOWING_OBSIDIAN)

# Create a gold block at goal position
mc.setBlock(goal.x, goal.y, goal.z, block.GOLD_BLOCK)

# Set player position next to base block
mc.player.setTilePos(base.x + 1, mc.getHeight(base.x + 1, base.z), base.z)

########################################
### Start game

## Initialize game state variables
# Is the player alive?
alive = True

# Is the goal reached
goalReached = False

# Has the mission succeeded
succeeded = False

# Post player instructions in Minecraft window
mc.postToChat("Find and destroy the gold block")
mc.postToChat("Beware of mines!!!")
mc.postToChat("Use your mine detector to avoid mines")

print("Game start")

# Store game start time
timeStart = time.time()

try:
    # Main game loop. Runs as long as player is alive and has not succeeded
    while alive and not succeeded:

        # get player position
        p = mc.player.getTilePos()

        # store player position in a Pt3D type object
        pos = Pt3D(p.x, p.y, p.z)

        ## Calculate distance to the nearest mine
        # set min distance to a large value
        distMin = 1000000.

        # do for each mine
        for mine in mines:
            # calculate distance to mine in horizontal plane
            dist = pos.distAxes(mine, 5)
            
            # if distance is smaller than current min distance
            if dist < distMin:
                # set distance as new min distance
                distMin = dist

        # display distance on mine detector (LEDs and buzzer)
        mineDetector.onValue(distMin)

        # if distance is smaller than mine trigger distance...
        if distMin <= distMineTrigger:
            # the player is dead!
            alive = False

        # check if the goal block is has been hit (block is air)
        if mc.getBlock(goal.x, goal.y, goal.z) == 0:

            # if block has just been hit
            if not goalReached:
                # set goal reached to True so messages appear only once
                goalReached = True
                # post messages to Minecraft chat
                mc.postToChat("Objective reached!")
                mc.postToChat("Now return to base (red block)")
                mc.postToChat("and destroy the block")

        # check if the base block is has been hit (block is air)
        if mc.getBlock(base.x, base.y, base.z) == 0:

            # if goal is already reached
            if goalReached:
                # set succeeded to true
                succeeded = True

            # if goal is not already reached, player must first reach the goal
            else:
                # post message to Minecraft chat
                mc.postToChat("You must fist find and destroy the gold block")
                # put back the base block
                mc.setBlock(base.x, base.y, base.z, block.GLOWING_OBSIDIAN)

    ## Game end

    # stop mine detector buzzer
    mineDetector.buzzer.stop()

    # case where the player is dead
    if not alive:
        # create explosion effect
        explosion(3)

        # post messages to Minecraft chat
        mc.postToChat("BOOM!!!")
        mc.postToChat(" ")
        mc.postToChat("Oh oh... You are dead!")
        print("Player is dead - cleaning up game")

        # set base and goal blocks to air
        clean()

        # blink mine detector leds for a few seconds
        mineDetector.blinkValue(0, 3)
        time.sleep(6)
        mineDetector.blinkOff()

    # case where the player has succeeded in completing the mission
    else:
        # post message to Minecraft chat
        mc.postToChat("Congratulations, you have succeeded!")

        # stop mine detector
        mineDetector.off()

        # calculate play time
        playTime = time.time() - timeStart
        # calculate minutes and seconds from play time
        minutes = str(int(playTime // 60))
        seconds = str(int(playTime % 60))
        # display play time to Minecraft chat
        mc.postToChat(("Time: " + minutes + "m " + seconds + "s"))

# Handle player interruption (Ctrl-C)
except KeyboardInterrupt:
    print("Game interrupted - cleaning up game")

# Close game - do clean-up and close running threads
finally:
    # set base and goal blocks to air
    clean()

    # stop mine detector
    mineDetector.off()
    mineDetector.buzzer.stop()

    print("Game closed successfully")
