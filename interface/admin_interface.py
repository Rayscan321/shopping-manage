"""
管理员接口
"""
from db import db_handler


def lock_user(username):
    """
    锁定用户
    :param username: 用户名
    :return: (boolean, str)
    """
    # 获取用户数据
    user_data = db_handler.select_data(username)
    if not user_data:
        return False, f"\n用户{username}不存在!"
    # 修改用户数据
    if user_data["locked"]:
        user_data["locked"] = False
        db_handler.save_data(user_data)
        return True, f"\n{username}已解锁!"
    user_data["locked"] = True
    # 保存用户数据
    db_handler.save_data(user_data)
    return True, f"\n{username}已被锁定!"
