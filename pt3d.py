# -*- coding: utf-8 -*-

# pt3d.py
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

class Pt3D:
    """A class defining a point in 3D space."""

    def __init__(self, x=0, y=0, z=0):
        """Constructor: Returns a Pt3D object instance.

        Keyword arguments:
        x: the x coordinate of the point
        y: the y coordinate of the point
        z: the z coordinate of the point
        """
        self.x = x
        self.y = y
        self.z = z

    def coords(self):
        """Returns a tuple containing the x, y, z coordinates of the point."""
        return (self.x, self.y, self.z)

    def dist3D(self, pt):
        """Returns the 3D distances to another point pt."""

        # Return 3D distance to point pt (Pythagorean theorem)
        return ((self.x - pt.x)**2 + (self.y - pt.y)**2 + (self.z - pt.z)**2)**.5

    def distAxes(self, pt, axes):
        """Returns the distance to another point along the specified axes or
        planes.

        Keyword arguments:
        pt: point to calculate distance to (Pt3D type object)
        axes: Axes to use for distance calculation
            1: x axis
            2: y axis
            4: z axis
            3: xy plane (1 + 2)
            5: xz plane (1 + 4)
            6: yz plane (2 + 4)
            7: 3D xyz (1 + 2 + 4)
        """
        # Set distances along axes to 0
        dx = 0
        dy = 0
        dz = 0
        if axes & 1 == 1:       # x axis is selected
            dx = self.x - pt.x  # Calculate distance along x axis
        if axes & 2 == 2:       # y axis is selected
            dy = self.y - pt.y  # Calculate distance along y axis
        if axes & 4 == 4:       # z axis is selected
            dz = self.z - pt.z  # Calculate distance along z axis

        # Return distance along selected axes (Pythagorean theorem)
        return (dx**2 + dy**2 + dz**2)**.5

    def length(self):
        """Returns vector's length from origin."""

        # Return 3D distance from origin (Pythagorean theorem)
        return (self.x**2 + self.y**2 + self.z**2)**.5
