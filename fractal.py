#! /usr/env/ipython3

"""
fractal.py begins the author's example of improving drawing
performance by drawing the canvas as an image using the
Python Imaging Library (PIM) to draw a fractal

The discussion begins on p. 271, section 10.7
"""

#
#

from tkinter import *
import Pmw
import AppShell
from PIL import Image
from PIL import ImageDraw
import os


# the Palette class is responsible for creating a random
# palette and generating an RGB list
class Palette:
    def __init__(self):
        self.palette = [(0, 0, 0), (255, 255, 255)]

    def getpalette(self):
        # flatten the palette
        palette = []
        for r, g, b in self.palette:
            palette = palette+[r, g, b]

        return palette

    def loadpalette(self, cells):
        import random
        for i in range(cells-2):
            self.palette.append((
                random.choice(range(0, 255)),
                random.choice(range(0, 255)),
                random.choice(range(0, 255))))


class Fractal(AppShell.AppShell):
    usecommandarea = 1
    appname = 'Fractal Demonstration'
    frameWidth = 780
    frameHeight = 580

    def createButtons(self):
        self.buttonAdd('Save',
                       helpMessage='Save current image',
                       statusMessage='Write current image as "out.gif"',
                       command=self.save)
        self.buttonAdd('Close',
                       helpMessage='Close Screen',
                       statusMessage='Exit',
                       command=self.close)

    def createDisplay(self):
        self.width = self.root.winfo_width()-10
        self.height = self.root.winfo_height()-95
        self.form = self.createcomponent('form', (), None,
                                         Frame, (self.interior(),),
                                         width=self.width,
                                         height=self.height)
        self.form.pack(side=TOP, expand=YES, fill=BOTH)

        # a new image is created specifying pixel mode (P) and is used
        # to instantiate the ImageDraw class, providing basic drawing
        # functions to the image. the image is filled with black
        # initially wit the setfill method
        self.im = Image.new('P', (self.width, self.height), 0)
        self.d = ImageDraw.ImageDraw(self.im)
        # self.d.setfill(0)
        self.label = self.createcomponent('label', (), None,
                                          Label, (self.form,),)
        self.label.pack()

    def initData(self):
        self.depth = 20
        self.origin = -1.4+1.0j
        self.range = 2.0
        self.maxDistance = 4.0
        self.ncolors = 256
        self.rgb = Palette()
        self.rgb.loadpalette(255)
        self.save = FALSE

    def createImage(self):
        self.updateProgress(0, self.height)
        for y in range(self.height):
            for x in range(self.width):
                z = 0j
                k = complex(self.origin.real +
                            float(x)/float(self.width)*self.range,
                            self.origin.imag -
                            float(y)/float(self.height)*self.range)
                # calculate z=(z+k) * (z+k) over and over
                for iteration in range(self.depth):
                    real_part = z.real+k.real
                    imag_part = z.imag+k.imag
                    del z
                    z = complex(real_part * real_part - imag_part *
                                imag_part, 2 * real_part * imag_part)
                    distance = z.real*z.real+z.imag*z.imag
                    if distance >= self.maxDistance:
                        # a color is selected and the corresponding
                        # pixel is set to that color
                        cidx = int(distance % self.ncolors)
                        self.pixel(x, y, cidx)
                        break
            self.updateProgress(y)
        self.updateProgress(self.height, self.height)
        # when complete, the palette is added to the image, saved as
        # a .gif file, and then the image is loaded as a PhotoImage
        self.im.putpalette(self.rgb.getpalette())
        self.im.save('out.gif')
        self.img = PhotiImage(file='out.gif')
        self.label['image'] = self.img

    # a very simple method to set the color of the ink and place the
    # pixel at the specified x, y coordinate
    def pixel(self, x, y, color):
        self.d.setink(color)
        self.d.point((x, y))

    def save(self):
        self.save = TRUE
        self.updateMessageBar('Saved as "out.gif"')

    def close(self):
        if not self.save:
            os.unlink('out.gif')
        self.quit()

    def createInterface(self):
        AppShell.AppShell.createInterface(self)
        self.createButtons()
        self.initData()
        self.createDisplay()


## ********************************************************************* ##
if __name__ == '__main__':
    fractal = Fractal()
    fractal.root.after(10, fractal.createImage())
    fractal.run()
