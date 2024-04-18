import os
import configparser


# 获取项目根路径
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# 获取CFG文件路径
CONFIG_PATH = os.path.join(BASE_DIR, "settings.cfg")

# 获取USER_DATA路径
config = configparser.ConfigParser()
config.read(CONFIG_PATH, encoding="utf-8-sig")
USER_DATA_DIR = config.get("path", "USER_DATA_DIR")
if not os.path.exists(USER_DATA_DIR):
    USER_DATA_DIR = os.path.join(BASE_DIR, "db", "user_data")

# 获取goods_data路径
GOODS_DATA_DIR = os.path.join(BASE_DIR, "db", "goods_data")

# 获取银行利率
RATE = config.getfloat("bank", "RATE")

# 获取日志存放路径
LOG_DIR = os.path.join(
    BASE_DIR, "logs"
)


LOGGING_DIC = {
    "version": 1.0,
    "disable_existing_loggers": False,
    # 日志格式
    "formatters": {
        "standard": {
            "format": "%(asctime)s %(threadName)s:%(thread)d [%(name)s] %(levelname)s [%(pathname)s:%(lineno)d] %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {
            "format": "%(asctime)s [%(name)s] %(levelname)s  %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "test": {
            "format": "%(asctime)s %(message)s",
        },
        "test1": {
            "format": "%(asctime)s %(message)s",
        },
    },
    "filters": {},
    # 日志处理器
    "handlers": {
        "console_debug_handler": {
            "level": "WARNING",  # 日志处理的级别限制
            "class": "logging.StreamHandler",  # 输出到终端
            "formatter": "simple",  # 日志格式
        },
        "file_user_handler": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",  # 保存到文件,日志轮转
            "filename": os.path.join(LOG_DIR, "user.log"),
            "maxBytes": 800,  # 日志大小 10M
            "backupCount": 3,  # 日志文件保存数量限制
            "encoding": "utf-8",
            "formatter": "standard",
        },
        "file_bank_handler": {
            "level": "DEBUG",
            "class": "logging.FileHandler",  # 保存到文件
            "filename": os.path.join(LOG_DIR, "bank.log"),  # 日志存放的路径
            "encoding": "utf-8",  # 日志文件的编码
            "formatter": "test",
        },
    },
    # 日志记录器
    "loggers": {
        "": {  # 导入时logging.getLogger时使用的app_name
            "handlers": ["file_user_handler"],  # 日志分配到哪个handlers中
            "level": "INFO",  # 日志记录的级别限制
            "propagate": False,  # 默认为True，向上（更高级别的logger）传递，设置为False即可，否则会一份日志向上层层传递
        },
        "bank_logger": {
            "handlers": ["file_bank_handler"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

if __name__ == "__main__":
    print(USER_DATA_DIR)
