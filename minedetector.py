# -*- coding: utf-8 -*-

# minedetector.py
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
from gpiozero import LED
from buzzlevel import BuzzLevel

class MineDetector:
    """A class defining a 4 LED scale (blue, green, yellow, red) that lights as
    function of a distance value. It is used in the MineField Minecraft game for
    Raspberry Pi to indicate the distance to the nearest mine. The class also
    controls a buzzer (BuzzLevel object type) that beeps a number of beeps
    corresponding to the number of LEDs lit.
    """

    def __init__(self, threshBlue, threshGreen, threshYellow, threshRed):
        """Constructor. Returns a MineDetector object.

        Keyword arguments:
        threshBlue: the distance threshold under which the blue LED lights
        threshGreen: the distance threshold under which the green LED lights
        threshYellow: the distance threshold under which the yellow LED lights
        threshRed: the distance threshold under which the red LED lights
        """
        self._threshBlue = threshBlue
        self._threshGreen = threshGreen
        self._threshYellow = threshYellow
        self._threshRed = threshRed
        self._ledBlue = LED(17)      # Blue LED on pin 17
        self._ledGreen = LED(27)     # Green LED on pin 27
        self._ledYellow = LED(22)    # Yellow LED on pin 22
        self._ledRed = LED(16)       # Red LED on pin 16
        self.buzzer = BuzzLevel()

    def onValue(self, value):
        """Turn LEDs and buzzer on corresponding to a distance value.

        Keyword arguments:
        value: the distance value
        """
        level = 0   # Initialize buzzer level to 0
        if value <= self._threshBlue:   # if value is smaller than blue threshold
            self._ledBlue.on()          # set blue LED to on
            level = 1                   # set level to 1
        else:                           # if value is greater than blue threshold
            self._ledBlue.off()         # set blue LED to off
        if value <= self._threshGreen:  # same for green LED...
            self._ledGreen.on()
            level = 2
        else:
            self._ledGreen.off()
        if value <= self._threshYellow: # and yellow LED...
            self._ledYellow.on()
            level = 3
        else:
            self._ledYellow.off()
        if value <= self._threshRed:    # red LED.
            self._ledRed.on()
            level = 4
        else:
            self._ledRed.off()
        self.buzzer.setLevel(level)    # set buzzer level

    def off(self):
        """Turn all LEDs and buzzer off."""
        self._ledBlue.off()
        self._ledGreen.off()
        self._ledYellow.off()
        self._ledRed.off()
        self.buzzer.setLevel(0)    # set buzzer level to 0 (off)

    def _blinkValue(self, value, freq):
        """Blink LEDs corresponding to a distance value.

        Keyword arguments:
        value: the distance value
        freq: blink frequency (/s)
        """
        self._blink = True   # set _blink attribute to True
        while self._blink:   # blink as long as blink attribute is True
            self.onValue(value)         # turn LEDs on
            time.sleep(1 / freq / 2)    # sleep
            self.off()                  # turn LEDs off
            time.sleep(1 / freq / 2)    # sleep

    def blinkValue(self, value, freq):
        """Launches _blinkValue method in a dedicated thread so it can run in
        the background while the calling program continues.

        Keyword arguments:
        value: the distance value
        freq: blink frequency (/s)
        """
        thread1 = threading.Thread(target = self._blinkValue, args = (value, freq))
        thread1.start()

    def blinkOff(self):
        """Sets the _blink attribute to False. The background thread will stop
        automatically at the end of the current loop."""
        self._blink = False
