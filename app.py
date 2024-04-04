import signal

from bot.config import LoggerSetup, config_loader
from bot.data import DateSourceUtils
from bot.server import HttpServer


def stopAppRunStatus(sig, frame):
    config_loader.App_Run_Status = False

# 初始化日志
LoggerSetup.setup_logging()
# 注册信号处理函数
signal.signal(signal.SIGINT, stopAppRunStatus)
# 初始化数据库
DateSourceUtils.initTable()
HttpServer.runHttpServer()
