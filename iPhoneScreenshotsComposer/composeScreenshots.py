from PIL import Image
import os

emptyiPhoneImageName = "EmptyiPhone.png"
centerBox = (31,117,333,567)

folder = os.getcwd() + "/"
imageSize = (centerBox[2] - centerBox[0], centerBox[3] - centerBox[1])
emptyiPhoneImage = Image.open(folder + emptyiPhoneImageName)

dirList = [fname for fname in os.listdir(folder) if fname != emptyiPhoneImageName and fname.lower().endswith(".png") and not fname.startswith("ss_")]
for fname in dirList:
    image = Image.open(folder + fname)
    image = image.resize(imageSize, Image.ANTIALIAS)
    newImage = emptyiPhoneImage.copy()
    newImage.paste(image, centerBox)
    newImage.save(folder+"ss_"+fname)
    