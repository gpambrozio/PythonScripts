#!/usr/bin/env python
# encoding: utf-8

import re
import os
import shutil
import subprocess
from bs4 import BeautifulSoup

## Tries to find docsetutil
possible_docsetutil_path = [
    "/Developer/usr/bin/docsetutil",
    "/Applications/Xcode.app/Contents/Developer/usr/bin/docsetutil",
]
docsetutil_path = [path for path in possible_docsetutil_path if os.path.exists(path)]
if len(docsetutil_path) == 0:
    print "Could not find docsetutil. Please check for docsetutil's location and set it inside the script."
    exit(1)

docsetutil_path = docsetutil_path[0]

## Script should run in the folder where the docs live
source_folder = os.getcwd() + "/"

## Find the Python version of the docs
python_version = None
f = open(source_folder + "index.html", 'r')
for line in f:
    search = re.search("Python v([0-9.]+) documentation", line)
    if search:
        python_version = search.group(1)
        break
f.close()

if python_version == None:
    print "I could not find Python's version in the index.html file. Are you in the right folder??"
    exit(1)

dest_folder = source_folder + ("python.%s.docset/" % python_version)


def is_something(tag, something):
    """ Function to help BeautifulSoup find our tokens """
    return (tag.name == "dt"
            and tag.has_key("id")
            and tag.parent.name == "dl"
            and tag.parent['class'][0] == something)


def collect(soup, what, identifier, names):
    """ Collects all nodes of a certain type from a BeautifulSoup document """
    whats = soup.find_all(lambda tag: is_something(tag, what))
    for n in whats:
        apple_ref = "//apple_ref/cpp/%s/%s" % (identifier, n["id"])
        new_tag = soup.new_tag("a")
        new_tag['name'] = apple_ref
        n.insert_before(new_tag)
        names.append(apple_ref)


## Clean up first
if os.path.exists(dest_folder):
    shutil.rmtree(dest_folder)

## Create all the necessary folder hierarchy
os.makedirs(dest_folder + "Contents/Resources/Documents/")
docset_folder = dest_folder
dest_folder = dest_folder + "Contents/"

## Find the module's index file. It's different in Python's 3 docs
possible_modindex_path = [
    "modindex.html",
    "py-modindex.html",
]
modindex_path = [path for path in possible_modindex_path if os.path.exists(source_folder + path)]
if len(modindex_path) == 0:
    print "Could not find modindex. Please check your doc folder structure and try again."
    exit(2)
modindex_path = modindex_path[0]

## Create Info.plist
info = open(dest_folder + "Info.plist", "w")
info.write("""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleIdentifier</key>
    <string>python.%s</string>
    <key>CFBundleName</key>
    <string>Python %s</string>
    <key>DocSetPlatformFamily</key>
    <string>python</string>
</dict>
</plist>
""" % (python_version, python_version))
info.close()

## Create Nodes.xml
dest_folder = dest_folder + "Resources/"
nodes = open(dest_folder + "Nodes.xml", "w")
nodes.write("""<?xml version="1.0" encoding="UTF-8"?>
<DocSetNodes version="1.0">
    <TOC>
        <Node type="folder">
            <Name>Modules Index</Name>
            <Path>%s</Path>
        </Node>
    </TOC>
</DocSetNodes>
""" % modindex_path)
nodes.close()

## Create the tokens file
tokens = open(dest_folder + "Tokens.xml", "w")
dest_folder = dest_folder + "Documents/"

## Copy some static files
shutil.copy(source_folder + "searchindex.js", dest_folder)
shutil.copy(source_folder + modindex_path, dest_folder)
shutil.copy(source_folder + "genindex-all.html", dest_folder)
shutil.copy(source_folder + "library/index.html", dest_folder)
shutil.copytree(source_folder + "_images", dest_folder + "_images")
shutil.copytree(source_folder + "_static", dest_folder + "_static")

## I'll hide the header because it makes no sense in a docset
## and messes up Dash
css = open(dest_folder + "_static/basic.css", "a+")
css.write("div.related {display:none;}\n")
css.close()
css = open(dest_folder + "_static/default.css", "a+")
css.write("a.headerlink {display:none;}\n")
css.close()

## Start of the tokens file
tokens.write("""<?xml version="1.0" encoding="UTF-8"?>
<Tokens version="1.0">
""")

## Collect pages first
pages = {}

## Collect pages from the modules index
f = open(source_folder + modindex_path, 'r')
for line in f:
    search = re.search("<a href=\"(.*)#.*?\"><tt class=\"xref\">(.*?)</tt>", line)
    if search:
        href = search.group(1)
        name = search.group(2)
        if not href in pages:
            pages[href] = []

        apple_ref = "//apple_ref/cpp/cat/%s" % name
        pages[href].append(apple_ref)

f.close()

## Collect pages from the general index
f = open(source_folder + "genindex-all.html", 'r')
for line in f:
    for search in re.finditer("(<dt>|, )<a href=\"([^#]+).*?\">", line):
        href = search.group(2)
        if not href in pages:
            pages[href] = []

f.close()

## Collect pages from the library index
f = open(source_folder + "library/index.html", 'r')
for line in f:
    for search in re.finditer("<a class=\"reference external\" href=\"([^#\"]+).*?\">", line):
        href = "library/" + search.group(1)
        if not ("http://" in href or "https://" in href or href in pages):
            pages[href] = []

f.close()

## Now write to tokens
for href, names in pages.items():

    soup = BeautifulSoup(open(source_folder + href))

    collect(soup, "class", "cl", names)
    collect(soup, "method", "clm", names)
    collect(soup, "classmethod", "clm", names)
    collect(soup, "function", "func", names)
    collect(soup, "exception", "cl", names)
    collect(soup, "attribute", "instp", names)

    if len(names) > 0:
        tokens.write("<File path=\"%s\">\n" % href)
        for name in names:
            tokens.write("\t<Token><TokenIdentifier>%s</TokenIdentifier><Anchor>%s</Anchor></Token>\n" % (name, name))
        tokens.write("</File>\n")

        newFile = dest_folder + href
        if not os.path.exists(os.path.dirname(newFile)):
            os.makedirs(os.path.dirname(newFile))
        newFile = open(newFile, "w")
        newFile.write(str(soup))
        newFile.close()

tokens.write("</Tokens>")
tokens.close()

subprocess.call([docsetutil_path, "index", docset_folder])

## Cleanup
os.remove(docset_folder + "Contents/Resources/Nodes.xml")
os.remove(docset_folder + "Contents/Resources/Tokens.xml")
