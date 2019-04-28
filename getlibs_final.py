#!/usr/bin/python3

# $1 is ~/getlibs2/getlibs3/test --- test folder that contains few files
# $2 is ~/getlibs2/getlibs3/ --- directory current directory
# $3 is 0



import sys
import os
import urllib.request
from urllib.request import urlretrieve 
import urllib.error
from urllib.error import URLError
import shutil
from zipfile import ZipFile


if len(sys.argv) != 4:
    print('Usage:')
    print(" sys.argv[0] GIT_DIR INST_ABSOLUTE_TARGET OVERWRITE_CSS")
    sys.exit(1)
else:
    GIT_DIR = sys.argv[1]
    libs = sys.argv[2]
    LIB_DIR = libs + '/lib'
    FORCE_CSS = sys.argv[3]
    print("Downloading libs to web directory 'LIB_DIR' ")

CSSLIST = []

WEB = LIB_DIR

os.mkdir(WEB)

if os.access(WEB, os.W_OK) is not True:
    print("Cannot write to WEB !")
    sys.exit(1)

websites = []
filepath = "url.txt"
file = open(filepath)
pat = file.readlines()
for url in pat:
    raw = url.strip()
    websites.append(raw)

os.chdir(WEB)

errors = []


for website in websites:
    if os.path.isfile(website.split('/')[-1]) is not True:
        try:
            wname = website.split('/')[-1]
            res = urllib.request.urlretrieve(website, wname)
            res
            print(res)
        except urllib.error.HTTPError as e:
            print('raise HTTPError')
            print(e.code)
            errors.append(website)
        except urllib.error.URLError as e:
            print('raise URLError')
            errors.append(website)
            
shutil.copy2(GIT_DIR + '/www-lib/treeviewer.js', os.getcwd())
shutil.copy2(GIT_DIR + '/www-lib/leaflet-phylogenscale.js', os.getcwd())
shutil.copy2(GIT_DIR + '/www-lib/leaflet-scrollbar.js', os.getcwd())


CSSLIST.append(GIT_DIR + '/www-lib/treeviewer.js')
CSSLIST.append(GIT_DIR + '/www-lib/leaflet-scrollbar.js')

for cssitm in CSSLIST:
    cssfile = cssitm.split('/')[0]
    if FORCE_CSS == 1:
        shutil.rmtree(cssfile)
    if os.path.isfile(cssfile) is not True:
        shutil.copy2(cssitm, os.getcwd())
    else:
        sys.exit(1)

if os.path.isfile("jquery-1.11.3.min.js") is not True:
    urllib.request.urlretrieve("http://code.jquery.com/jquery-1.11.3.min.js", 'jquery-1.11.3.min.js')
    os.symlink("jquery-1.11.3.min.js", 'jquery.min.js')
if os.path.isfile("leaflet.js") is not True:
    try:
        urllib.request.urlretrieve("http://cdn.leafletjs.com/leaflet/v1.0.0-rc.2/leaflet.zip", 'leaflet.zip')
        if os.path.isfile("leaflet.zip") is not True:
            sys.exit(1)
        else:
            with ZipFile("leaflet.zip", 'r') as zipObj:
                zipObj.extractall()
                os.remove("leaflet.zip")
    except urllib.error.HTTPError as e:
        sys.exit(1)

for file in errors:
    print("Download unsuccessful from " + file)

if len(errors) != 0:
    sys.exit(1)
