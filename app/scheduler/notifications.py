from app.scheduler.funtions import *
from icecream import ic
from datetime import datetime
from config import time_from, time_to


def add_job_scheduler(scheduler):
    # scheduler.add_job(ic, "cron", hour="13", minute=45)
    scheduler.add_job(send_to_teacher, 'cron', day_of_week="1-5", hour=time_from.hour,
                      minute=time_from.minute, args=["запись открыта"])
    scheduler.add_job(send_to_teacher, 'cron', day_of_week="1-5", hour=time_to.hour,
                      minute=time_to.minute, args=["запись закрыта"])
    scheduler.add_job(send_to_vosp, 'cron', day_of_week="1-5", hour=time_from.hour,
                      minute=time_from.minute, args=["запись открыта"])
    scheduler.add_job(send_to_vosp, "cron", day_of_week="1-5", hour=time_to.hour,
                      minute=time_to.minute, args=["запись закрыта"])
    scheduler.add_job(send_notifications_vosp, "cron", day_of_week="1-5", hour=time_to.hour,
                      minute=time_to.minute)
