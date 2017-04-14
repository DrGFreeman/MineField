# -*- coding: utf-8 -*-

# buzzlevel.py
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

import threading
import time
from gpiozero import Buzzer

class BuzzLevel:
    """A buzzer class for use in MineField Minecraft game for Raspbery Pi. The
    buzzer emits a number of short beeps corresponding to the specified level
    (0 to 4). An active buzzer must be connected to GPIO pin 4."""

    def __init__(self):
        """Constructor. Returns a BuzzLevel object instance"""
        self._buzzer = Buzzer(4)    # gpiozero Buzzer object on pin 4.
        self._onTime = .01          # beep duration
        self._offTime = .19         # beep silence duration
        self._level = 0             # beep level initialized to 0
        self._active = False        # object active state initialized to False
        self.run()                  # activate object

    def _beep(self, on):
        """Beeps the buzzer once followed by a silence.

        Keyword arguments:
        on: Produces a beep if True, produces a silence if False.
        """
        if on:
            self._buzzer.on()
            time.sleep(self._onTime)
            self._buzzer.off()
            time.sleep(self._offTime)
        else:
            time.sleep(self._onTime + self._offTime)

    def _beepLevel(self):
        """Beeps the buzzer a number of times set by the level attribute followed
        by a number of silences so that the total duration is always constant."""

        for i in range(self._level):
            self._beep(True)
        for i in range(5 - self._level):
            self._beep(False)

    def run(self):
        """Launches the _run method in a dedicated thread so it can run in the
        background while the calling program continues.
        """

        if not self._active:
            thread1 = threading.Thread(target = self._run, args = [])
            thread1.start()

    def _run(self):
        """Executes the beepLevel method as long as the _active attribute is
        True."""

        self._active = True
        while self._active:
            self._beepLevel()

    def setLevel(self, level):
        """Sets the buzzer _level attribute.

        Keyword arguments:
        level: the number of beeps to be produced (0 to 4)
        """
        try:
            if type(level) != int:  # check that level is an integer
                raise TypeError("level must be an integer.")
            elif level >=0 and level <= 4: # check that level is between 0 and 4
                self._level = level # set _level attribute
            else:
                raise ValueError("level must be between 0 and 4.")

        except ValueError:
            raise

        except TypeError:
            raise

    def stop(self):
        """Sets the _active attribute to False. The background thread will stop
        automatically at the end of the current loop."""
        self._active = False
