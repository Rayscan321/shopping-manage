"""
公共方法
"""
import hashlib
from core import core


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


if __name__ == "__main__":
    print(pwd_to_sha256("123456"))
