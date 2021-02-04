import os
import time
import aircv as ac
import pymouse
import pykeyboard
from PIL import ImageGrab
m = pymouse.PyMouse()
k = pykeyboard.PyKeyboard()

scream_locat = "./tmp/scream.jpg"

def install_pack():
    pack_list = ["PyUserInput", "apschedule", "Pillow", "aircv"]
    packs = " ".join(pack_list)
    os.system(f"python -m pip install --upgrade {packs}")

def ctrlnimble(*args):
    time.sleep(1)
    k.press_key(k.control_key)
    for i in args:
        k.tap_key(i)
    k.release_key(k.control_key)

def copyall():
    ctrlnimble('a', 'c')

def copy():
    ctrlnimble('c')

def stick():
    ctrlnimble('v')

def cutscream():
    img = ImageGrab.grab()
    img.save(scream_locat)

def recount(result):
    return int(result[0]/1824*1042),int(result[1]/2736*1563)
    # return int(result[0]),int(result[1])

def getlocation(imsearch):
    cutscream()
    scream = ac.imread(scream_locat)
    imsearch = ac.imread(imsearch)

    result = ac.find_template(scream, imsearch)
    if result == None:
        return None
    else:
        return recount(result['result'])

def self_open(location, status):
    for i in status:
        is_open = getlocation(location+i)
        if is_open != None:
            m.click(is_open[0],is_open[1])
            time.sleep(1)
            return True
    return False

def alert(name):
    os.system(name)

if __name__ == "__main__":
    install_pack()