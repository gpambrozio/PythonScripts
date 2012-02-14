#!/usr/bin/env python
# encoding: utf-8
"""
composeScreenshots.py

Created by Gustavo Ambrozio on 2012-02-14.
"""

from PIL import Image
import os

def main():
    emptyiPhoneImageName = "EmptyiPhone.png"
    centerBox = (31,117,333,567)

    folder = os.getcwd() + "/"
    imageSize = (centerBox[2] - centerBox[0], centerBox[3] - centerBox[1])
    emptyiPhoneImage = Image.open(folder + emptyiPhoneImageName)

    dirList = [fname for fname in os.listdir(folder) if fname != emptyiPhoneImageName and fname.lower().endswith(".png") and not fname.startswith("ss_")]
    for fname in dirList:
        print "Composing %s" % fname
        image = Image.open(folder + fname)
        image = image.resize(imageSize, Image.ANTIALIAS)
        newImage = emptyiPhoneImage.copy()
        newImage.paste(image, centerBox)
        newImage.save(folder+"ss_"+fname)

if __name__ == '__main__':
    main()
