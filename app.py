import logging
import signal

from bot.config import LoggerSetup, config_loader
from bot.data import DateSourceUtils
from bot.server import HttpServer

logging.getLogger("urllib3").setLevel(logging.WARNING)


def stopAppRunStatus(sig, frame):
    config_loader.App_Run_Status = False


# 注册信号处理函数
signal.signal(signal.SIGINT, stopAppRunStatus)

DateSourceUtils.initTable()
LoggerSetup.setup_logging()
HttpServer.runHttpServer()
