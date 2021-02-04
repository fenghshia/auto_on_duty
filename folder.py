from util import *


class folder:

    def __init__(self):
        self.location = "./folder"

    def self_open(self):
        status = ["/single_open.png", "/single_close.png", "/multi_open.png", "/multi_close.png"]
        self_open(self.location, status)
        self_open(self.location, ["/cut_mini_folder.png"])
    
    def get_key(self):
        self.self_open()
        self_open(self.location, ["/key_locat.png"])
        copy()
    
    def get_vrbt(self):
        self.self_open()
        self_open(self.location, ["/vrbt_locat.png"])
        copy()
        

if __name__ == "__main__":
    folder().get_vrbt()