"""
公共方法
"""
import hashlib
import logging.config
from core import core
from conf import settings


# 登录认证装饰器
def login_auth(func):
    def wrapper(*args, **kwargs):
        if not core.logged_user:
            print("\n请先登录")
            core.login()
        else:
            return func(*args, **kwargs)
    return wrapper


# 密码加密
def pwd_to_sha256(pwd):
    sha256 = hashlib.sha256()
    sha256.update(pwd.encode("utf-8"))
    sha256.update(b"123456")
    return sha256.hexdigest()


# 日志记录功能
def get_logger(logger_name):
    # 加载日志配置字典
    logging.config.dictConfig(settings.LOGGING_DIC)

    # 获取logger
    logger = logging.getLogger(logger_name)
    return logger

if __name__ == "__main__":
    print(pwd_to_sha256("123456"))
