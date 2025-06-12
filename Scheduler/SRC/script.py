# スタートさせたいとき
# nohup python script.py > output.log 2>&1 &
# 終了させたいとき
# kill [id]

from notifypy import Notify
from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime


def notify_break_msg():
    now=datetime.now()
    hour=now.hour()
    if 5<= hour <=21:
      notification = Notify()
      notification.title="お知らせ"
      notification.message="休憩をとりましょう"
      notification.send()

scheduler=BlockingScheduler()
scheduler.add_job(
    notify_break_msg,
    "interval",
    minutes=50,
    hour='5-21',
    id="break_msg_job"
)

scheduler.start()

