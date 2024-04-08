"""
用户接口
"""
from db import db_handler


# 注册接口
def register(username, password, balance=0, is_admin=False):
    """
    用户接口
    :param username: 用户名 str
    :param password: 密码 str
    :param balance: 初始余额 int
    :param is_admin: 是否管理员 bool
    :return: (boolean, str)
    """
    # 调用数据处理层的查询功能，判断用户名是否存在
    if db_handler.select_data(username, data=False):
        return False, "\n用户名已存在!"
    # 组织用户字典
    user_data = {
        "username": username,
        "password": password,
        "balance": balance,
        "shopping_cart": {},
        "flow": [],
        "is_admin": is_admin,
        "locked": False,
    }
    # 调用数据处理层，保存用户数据
    db_handler.save_data(user_data)
    return True, "\n注册成功!"


# 登录接口
def login(username, password):
    """
    登录接口
    :param username: 用户名 str
    :param password: 密码 str
    :return: (boolean, str, boolean)
    """
    # 调用数据处理层的查询功能，判断用户名是否存在
    user_data = db_handler.select_data(username)
    if not user_data:
        return False, "\n用户名不存在!", False
    # 判断密码是否正确
    if user_data["password"] != password:
        return False, "\n密码错误!", False
    # 判断用户是否被锁定
    if user_data["locked"]:
        return False, f"\n该账号{username}已被锁定!", False

    return True, f"\n{username}登录成功!", user_data.get("is_admin")
