from util import alert
from time import sleep
from flask import Flask
from config import *
from folder import folder
from vscode import context
from weixin import zhonghualong, zhibanqun
from socket import gethostname, gethostbyname
from browser import key, vrbt
from keydata import jetty_data, webgate, frontpage, login, restime, search, vrbt1, vrbt2, vrbt3, vrbt4
from datetime import datetime
from autoemail import autoemail
from flask_apscheduler import APScheduler
from apscheduler.schedulers.blocking import BlockingScheduler


class config:
    SCHEDULER_API_ENABLED = True

app=Flask(__name__)
app.config.from_object(config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
mail = autoemail()

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
            mail.build_msg(f"{i.name}数据异常")
            return False
        mail.build_msg(f"{i.name}数据正常")
    return True

    
# 整体流程
now = datetime.now()
@scheduler.task(args=[key_cookie, vrbt_cookie],
                start_date=f"{now.year}-{now.month}-{duty_day} 09:30:10",
                end_date=f"{now.year}-{now.month}-{duty_day+1} 09:00:20",
                trigger="interval",
                minutes=30,
                id='basejob')
def workflow(key_cookie, vrbt_cookie):
    mail.build_msg(now)
    if webdata(key_cookie, vrbt_cookie):
        sendmsg()
        mail.build_msg("微信消息已发送")
    else:
        alert("alertmusic.mp3")
        mail.build_msg("告警已触发")
    mail.send()

@scheduler.task(args=["外部插入"], end_date="2021-02-04 17:50:20", trigger="interval", minutes=1, id='testjob')
def test(s):
    pass

# 告警接口
@app.route("/alert")
def api_alert():
    alert("alertmusic.mp3")
    return "success"


if __name__ == "__main__":
    localIP = gethostbyname(gethostname())
    app.run(host="192.168.151.196",
            port=6900,
            debug=False)



