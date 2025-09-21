# 代码生成时间: 2025-09-22 00:24:25
import asyncio
from sanic import Sanic, response
from sanic.exceptions import ServerError
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.jobstores.memory import MemoryJobStore
# 扩展功能模块
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR

# 定义定时任务调度器
class ScheduledTask:
    def __init__(self, app: Sanic):
        self.app = app
        self.scheduler = AsyncIOScheduler(jobstores={'default': MemoryJobStore()},
                                             executor='default')
        self.scheduler.start()

    def add_task(self, func, trigger: IntervalTrigger, args=None, kwargs=None, id=None):
        """
        添加定时任务

        Args:
            func: 任务函数
            trigger: 触发器
            args: 函数参数列表
# TODO: 优化性能
            kwargs: 函数关键字参数字典
            id: 任务ID
        """
        job = self.scheduler.add_job(func, trigger, args=args, kwargs=kwargs, id=id)
        return job

    def remove_task(self, job_id):
        """
        移除定时任务
# 增强安全性

        Args:
            job_id: 任务ID
        """
        self.scheduler.remove_job(job_id)

    def get_all_jobs(self):
        """
        获取所有定时任务
        """
        return self.scheduler.get_jobs()

    # 定时任务回调函数
    def job_executed(self, event):
        """
        任务执行成功回调
        """
        print(f"Job {event.job_id} executed successfully")

    def job_error(self, event):
# 优化算法效率
        "