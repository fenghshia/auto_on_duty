import datetime
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler import events
import math


# 只执行一次 
def basecode():
    """
    BlockingScheduler 方法会阻塞主进程
    multiprocess 不能控制此方法
    """

    def job(text):
        print(f"job run at {datetime.datetime.now()} with input {text}")

    scheduler = BlockingScheduler()
    scheduler.add_job(job, "date", minutes=30, args=[], id='basejob')
    scheduler.start()

    print("主进程未被占用")


# 后台执行
def backrun():

    def job1(text):
        print(f"job backrun at {datetime.datetime.now()} with input {text}")

    def job2(text):
        print(f"job backrun at {datetime.datetime.now()} with input {text}")
        raise TypeError

    def eventlistener(event):
        print(event)
        x = int(math.log2(event.code))
        print(events.__all__[x])
    
    scheduler = BackgroundScheduler()
    scheduler.add_listener(eventlistener)
    scheduler.add_job(job1, "interval", seconds=1, args=["1后台运行测试"],id="backrun1")
    scheduler.add_job(job2, "interval", seconds=5, args=["2后台运行测试"],id="backrun2")
    scheduler.start()

    print("主进程未被占用")


if __name__ == "__main__":
    backrun()
    i = 0
    while True:
        i += 1
        time.sleep(1)
        if i == 10:
            break
