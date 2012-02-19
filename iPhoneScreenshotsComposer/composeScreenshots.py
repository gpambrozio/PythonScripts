#!/usr/bin/env python
# encoding: utf-8
"""
composeScreenshots.py

Created by Gustavo Ambrozio on 2012-02-14.
"""

import os
from PIL import Image


def main():
    empty_iPhone_image_name = "EmptyiPhone.png"
    center_box = (31, 117, 333, 567)

    folder = os.getcwd() + "/"
    image_size = (center_box[2] - center_box[0], center_box[3] - center_box[1])
    empty_iPhone_image = Image.open(folder + empty_iPhone_image_name)

    dirList = [fname for fname in os.listdir(folder)
                     if fname != empty_iPhone_image_name
                        and fname.lower().endswith(".png")
                        and not fname.startswith("ss_")]
    for fname in dirList:
        print "Composing %s" % fname
        image = Image.open(folder + fname)
        image = image.resize(image_size, Image.ANTIALIAS)
        new_image = empty_iPhone_image.copy()
        new_image.paste(image, center_box)
        new_image.save(folder + "ss_" + fname)

if __name__ == '__main__':
    main()
