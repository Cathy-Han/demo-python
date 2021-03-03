from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from data import DataPrepare
from quota import Quota

# 输出时间
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #拉取数据
    dp=DataPrepare()
    dp.Load()
    #计算指标
    qt=Quota(48)
    qt.Show()
# BlockingScheduler
scheduler = BlockingScheduler()
scheduler.add_job(job, 'cron', day_of_week='1-5', minute=0)
scheduler.start()