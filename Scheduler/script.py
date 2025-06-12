from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

def display_hello(message):
    print(datetime.now(),f"こんにちは{message}")


scheduler=BlockingScheduler()
scheduler.add_job(
    display_hello,
    "cron",
    hour=13,
    minute=2,
    args=["20時18分に実行"],
    id="hello_job"
)
scheduler.start()