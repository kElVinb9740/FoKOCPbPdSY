# 代码生成时间: 2025-08-06 23:48:59
import asyncio
from datetime import datetime, timedelta
import schedule
from sanic import Sanic, response
from sanic.exceptions import ServerError
from sanic.request import Request
from sanic.response import json
from typing import Callable

# 定时任务调度器类
class ScheduledTaskScheduler:
    def __init__(self):
        self.scheduler = schedule.Scheduler()
        self.tasks = {}

    # 添加任务到调度器
    def add_task(self, task_id: str, task_func: Callable, interval: int = 1):
        """
        添加任务到调度器中。

        参数:
        task_id (str): 任务的唯一标识符。
        task_func (Callable): 要执行的任务函数。
        interval (int): 任务执行的时间间隔，单位为秒，默认为1秒。
        """
        self.tasks[task_id] = self.scheduler.every(interval).seconds.do(task_func)
        print(f"Task {task_id} added with interval {interval} seconds.")

    # 启动调度器
    def start(self):
        """
        启动调度器以执行任务。
        """
        self.scheduler.start()
        print("Scheduler started.")

# 定义Sanic应用程序
app = Sanic("ScheduledTaskScheduler")
scheduler = ScheduledTaskScheduler()

# 示例定时任务函数
def my_scheduled_task():
    """
    一个示例定时任务函数，打印当前时间。
    """
    print(f"Task executed at {datetime.now()}")

# 添加示例任务到调度器
scheduler.add_task("example_task", my_scheduled_task, interval=5)

# 启动调度器
@app.listener('after_server_start')
async def setup(app: Sanic, loop: asyncio.BaseEventLoop):
    """
    当服务器启动后，启动调度器。
    """
    scheduler.start()

# 定义一个API端点用于检查服务器状态
@app.route("/status", methods=["GET"])
async def status(request: Request):
    """
    返回服务器状态的API端点。
    """
    try:
        return response.json({
            "status": "running",
            "message": "Scheduler is running successfully."
        })
    except Exception as e:
        raise ServerError("Failed to get server status