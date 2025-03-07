from app.scheduler.funtions import *
from icecream import ic
from datetime import datetime, timedelta
from config import time_from, time_to


def add_job_scheduler(scheduler):
    datt_now = datetime.now()
    datt = datetime(datt_now.year, datt_now.month,
                    datt_now.day, time_to.hour, time_to.minute, 0)
    # scheduler.add_job(CheckRemainders, 'cron', day_of_week="0-5", hour=(datt - timedelta(minutes=5)).hour,
    #                   minute=(datt - timedelta(minutes=5)).minute)
    scheduler.add_job(send_to_teacher, 'cron', day_of_week="0-5", hour=time_from.hour,
                      minute=time_from.minute, args=["запись открыта"])
    scheduler.add_job(send_to_teacher, 'cron', day_of_week="0-5", hour=time_to.hour,
                      minute=time_to.minute, args=["запись закрыта"])
    scheduler.add_job(send_to_vosp, 'cron', day_of_week="0-5", hour=time_from.hour,
                      minute=time_from.minute, args=["запись открыта"])
    scheduler.add_job(send_to_vosp, "cron", day_of_week="0-5", hour=time_to.hour,
                      minute=time_to.minute, args=["запись закрыта"])
    scheduler.add_job(send_notifications, "cron", day_of_week="0-5", hour=(datt - timedelta(minutes=45)).hour,
                      minute=(datt - timedelta(minutes=45)).minute)
    scheduler.add_job(send_notifications, "cron", day_of_week="0-5", hour=16,
                      minute=0)
    scheduler.add_job(send_notifications_teacher, "cron", day_of_week="0-5", hour=12,
                      minute=1)
    scheduler.add_job(send_notifications_teacher, "cron", day_of_week="0-5", hour=13,
                      minute=6)
    scheduler.add_job(del_message, "cron", hour=21, minute=2)
