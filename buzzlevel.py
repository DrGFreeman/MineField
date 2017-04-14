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
        self.buzzer = Buzzer(4) # gpiozero Buzzer object on pin 4.
        self.onTime = .01       # beep duration
        self.offTime = .19      # beep silence duration
        self.level = 0          # beep level initialized to 0
        self.active = False     # object active state initialized to False
        self.run()              # activate object

    def beep(self, on):
        """Beeps the buzzer once followed by a silence.

        Keyword arguments:
        on: Produces a beep if True, produces a silence if False.
        """
        if on:
            self.buzzer.on()
            time.sleep(self.onTime)
            self.buzzer.off()
            time.sleep(self.offTime)
        else:
            time.sleep(self.onTime + self.offTime)

    def beepLevel(self):
        """Beeps the buzzer a number of times set by the level attribute followed
        by a number of silences so that the total duration is always constant."""

        for i in range(self.level):
            self.beep(True)
        for i in range(5 - self.level):
            self.beep(False)

    def run(self):
        """Launches the _run method in a dedicated thread so it can run in the
        background while the calling program continues."""

        if not self.active:
            thread1 = threading.Thread(target = self._run, args = [])
            thread1.start()

    def _run(self):
        """Executes the beepLevel method as long as the active attribute is
        True."""

        self.active = True
        while self.active:
            self.beepLevel()

    def setLevel(self, level):
        """Sets the buzzer level attribute.

        Keyword arguments:
        level: the number of beeps to be produced (0 to 4)
        """
        self.level = level

    def stop(self):
        """Sets the active attribute to False. The background thread will stop
        automatically at the end of the current loop."""
        self.active = False
