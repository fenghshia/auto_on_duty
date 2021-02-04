from util import alert
from time import sleep
from weixin import zhonghualong, zhibanqun
from vscode import context
from folder import folder
from browser import key, vrbt
from keydata import jetty_data, webgate, frontpage, login, restime, search, vrbt1, vrbt2, vrbt3, vrbt4
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler


# 发送消息
def sendmsg():
    wx = zhibanqun()
    ct = context()
    fd = folder()
    ky = key()
    vt = vrbt()

    # 1.刷新
    ky.flash()
    vt.flash()

    # 2.复制文本
    ct.copycontext()
    wx.self_stick()

    # 3.截图
    ky.cut()
    vt.cut()

    # 4.复制图片
    fd.get_key()
    wx.self_stick()
    fd.get_vrbt()
    wx.self_stick()
    wx.send()


# 界面数据
def webdata(key_cookie, vrbt_cookie):
    config = {
        "jetty": 80,
        "login": {"flag": "s",
                  "index": 0,
                  "value": 0.8},
        "restime": {"flag": "l",
                    "index": 0,
                    "value": 1000},
        "search": {"flag": "l",
                   "index": 0,
                   "value": 3000}
    }
    keydata = [
        jetty_data(config, key_cookie),
        webgate(config, key_cookie),
        frontpage(config, key_cookie),
        login(config, key_cookie),
        restime(config, key_cookie),
        search(config, key_cookie),
        vrbt1(config, vrbt_cookie),
        vrbt2(config, vrbt_cookie),
        vrbt3(config, vrbt_cookie),
        vrbt4(config, vrbt_cookie)
    ]
    for i in keydata:
        i.judge()
        if i.status == False:
            return False
    return True


# 时间规整
def plantime():
    now = datetime.now()
    if now.minute <=30:
        sleep((31 - now.minute)*60)
    elif 30 < now.minute <= 60:
        sleep((61 - now.minute)*60)
    
# 整体流程
def workflow(key_cookie, vrbt_cookie):
    if webdata(key_cookie, vrbt_cookie):
        sendmsg()
    else:
        alert("alertmusic.mp3")


def test():
    print(f"{datetime.now()}还在执行!")
if __name__ == "__main__":
    key_cookie = "SL_GWPT_Show_Hide_tmp=1; SL_G_WPT_TO=en; SL_wptGlobTipTmp=1; grafana_session=342bd7aa24c9bd9ee5d186dd2fd4d893"
    vrbt_cookie = "SL_G_WPT_TO=zh; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; grafana_session=a56812284747bf1a4f0a32cf1a3d20cd"
    # plantime()
    # workflow(key_cookie, vrbt_cookie)
    scheduler = BlockingScheduler()
    # scheduler.add_job(workflow, "interval", minutes=30, args=[key_cookie, vrbt_cookie], id='basejob')
    scheduler.add_job(test, "interval", minutes=1, start_date="2021-02-03 17:59:00", end_date="2021-02-03 18:05:00", id='basejob')
    scheduler.start()



