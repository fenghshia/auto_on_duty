from util import *


class browser:

    def __init__(self):
        self.location = "./browser"

    def self_open(self):
        status = ["/open.png", "/close.png"]
        self_open(self.location, status)

class key(browser):

    def __init__(self):
        super().__init__()
        self.clocation = self.location + "/key"
    
    def self_open(self):
        status = ["/open.png", "/close.png"]
        r = self_open(self.clocation, status)
        if r == False:
            super().self_open()
            self_open(self.clocation, status)
    
    def flash(self):
        self.self_open()
        k.tap_key(k.function_keys[5])
    
    def cut(self):
        self.self_open()
        img = ImageGrab.grab()
        cut = img.crop([120, 280, 2750, 1504])
        cut.save("./cut/key.jpg")


class vrbt(browser):

    def __init__(self):
        super().__init__()
        self.clocation = self.location + "/vrbt"
    
    def self_open(self):
        status = ["/open.png", "/close.png"]
        r = self_open(self.clocation, status)
        if r == False:
            super().self_open()
            self_open(self.clocation, status)
    
    def flash(self):
        self.self_open()
        k.tap_key(k.function_keys[5])
    
    def cut(self):
        self.self_open()
        img = ImageGrab.grab()
        cut = img.crop([120, 280, 2736, 1504])
        cut.save("./cut/vrbt.jpg")


if __name__ == "__main__":
    vrbt().cut()
    key().cut()