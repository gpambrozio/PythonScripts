# My Python Scripts

I've been playing with Python for a few weeks now and, at least for scripting jobs it's becoming my favorite language to use.

This is my collection of Python scripts that maybe someone might like to use. They'll be inside folders when there's more than one file needed or on the root when it's a simple one file script.

## iPhoneScreenshotsComposer

Simple script to turn screenshots taken from the iPhone simulator or from an iPhone and composing it with an iPhone4 image:

Source
![Result of the script](https://github.com/gpambrozio/PythonScripts/raw/master/iPhoneScreenshotsComposer/Push.png)

Result
![Result of the script](https://github.com/gpambrozio/PythonScripts/raw/master/iPhoneScreenshotsComposer/ss_Push.png)

### Pre-requisites

This script uses PIL (http://www.pythonware.com/products/pil/). The easiest way to install PIL is using pip:

    sudo pip install PIL

### Using the script

To use the script place your screenshot files in the same folder as the script and the EmptyiPhone.png file and run it. The script will create new files with ss_ prefixes for all .png files found in the folder.

### Changing the iPhone image

To use a different image or to adapt the script for an iPad screen for example, change the EmptyiPhone image or the name of the image in the script and change the coordinates used to paste the original screen shots. I plan to automate this step by analyzing the image and finding the transparent rectangle in the middle but so far this is a manual step.
