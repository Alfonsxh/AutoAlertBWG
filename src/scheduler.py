#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytz

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


def _init_scheduler() -> BackgroundScheduler:
    """初始化后台任务"""
    executors = {
        'default': ThreadPoolExecutor(20),
        'processpool': ProcessPoolExecutor(5)
    }
    job_defaults = {
        'coalesce': True,  # 合并因各种原因导致未执行的任务同一时间提交时，只会执行一次
        'max_instances': 1,  # 同一个job同一时间最多一个实例，例如耗时为10分钟的job，每隔1分钟执行一次，在0-10分钟内，只执行一个该job的实例
        'misfire_grace_time': 60  # job提交时间超过预执行时间60s，不执行该job。例如 14：00 执行的任务，在14：02 被提交，超过了60s，不执行该任务
    }

    # jobstores = {
    #     'default': RedisJobStore(jobs_key='cloud_scheduler',
    #                              run_times_key='dispatched_trips_running',
    #                              host=env_settings.REDIS_HOST,
    #                              port=env_settings.REDIS_PORT,
    #                              password=env_settings.REDIS_PASSWORD)
    # }

    # 这里使用BackgroundScheduler即可
    _scheduler = BackgroundScheduler(executors=executors,
                                     job_defaults=job_defaults,
                                     # jobstores=jobstores,
                                     timezone=pytz.timezone(u'Asia/Shanghai'))

    _scheduler.start()
    return _scheduler


scheduler = _init_scheduler()
