from util import *
from datetime import datetime


class vscode:

    def __init__(self):
        self.location = "./vscode"

    def self_open(self):
        status = ["/open.png", "/close.png"]
        self_open(self.location, status)

class context(vscode):

    def __init__(self):
        super().__init__()
        self.clocation = self.location + "/context"
    
    def self_open(self):
        status = ["/open.png", "/close.png"]
        r = self_open(self.clocation, status)
        if r == False:
            super().self_open()
            self_open(self.clocation, status)
    
    def general_content(self):
        with open('content.txt', 'w', encoding='utf-8') as f:
            time = datetime.now()
            print(f"{time} : 开始执行自动化值班")
            m = time.minute
            if m < 30:
                content = "客户端后台系统 {}月{}日{}:30 - {}:00 系统运行正常"
                if time.hour == 0:
                    h1 = "023"
                    h2 = "024"
                else:
                    h1 = f"0{time.hour-1}"
                    h2 = f"0{time.hour}"
            else:
                content = "客户端后台系统 {}月{}日{}:00 - {}:30 系统运行正常"
                h1 = f"0{time.hour}"
                h2 = f"0{time.hour}"
            M = time.month
            d = time.day
            content = content.format(M, d, h1[-2:], h2[-2:])
            f.write(content)
    
    def copycontext(self):
        self.general_content()
        self.self_open()
        x, y = recount([1660, 770])
        m.click(x, y)
        copyall()


if __name__ == "__main__":
    context().copycontext()