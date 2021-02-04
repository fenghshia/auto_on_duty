from util import *

class weixin:

    def __init__(self):
        self.location = "./weixin"

    def self_open(self):
        status = ["/open.png", "/close.png", "/alert.png"]
        self_open(self.location, status)

    def send(self):
        k.press_key(k.enter_key)

class zhibanqun(weixin):

    def __init__(self):
        super().__init__()
        self.clocation = self.location + "/zhibanqun"
    
    def self_open(self):
        status = ["/open.png", "/close.png"]
        r = self_open(self.clocation, status)
        if r == False:
            super().self_open()
            self_open(self.clocation, status)

    def self_stick(self):
        self.self_open()
        stick()

class zhonghualong(weixin):

    def __init__(self):
        super().__init__()
        self.clocation = self.location + "/zhonghualong"
    
    def self_open(self):
        status = ["/open.png", "/close.png"]
        r = self_open(self.clocation, status)
        if r == False:
            super().self_open()
            self_open(self.clocation, status)

    def self_stick(self):
        self.self_open()
        stick()

if __name__ == "__main__":
    # autosendmsg(context(), weixin(), edge(), filefolder())
    zhibanqun().self_open()
    # 生成文本内容:ok
    # 复制文本内容:ok
    # 打开微信:ok
    # 粘贴文本内容:ok
    # 打开edge:
    # 切换窗口
    # 截屏
    # 裁剪
    # 打开文件夹
    # 复制图片
    # 打开微信
    # 粘贴图片
    # 打开edge
    # 切换