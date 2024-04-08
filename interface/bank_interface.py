"""
银行接口
"""
from datetime import datetime
from db import db_handler
from conf import settings


# 充值接口
def recharge(logged_user, money):
    """
    充值接口
    :param logged_user: 已登录用户
    :param money: 充值金额
    :return: (boolean, str)
    """
    # 获取用户数据
    user_data = db_handler.select_data(logged_user)
    if not user_data:
        return True, "\n用户不存在!"
    # 计算手续费
    money = money * settings.RATE
    # 修改余额
    user_data["balance"] += money
    # 记录流水
    user_data["flow"].append(f"{datetime.now()}:{logged_user}充值{money}元成功!账户余额为{user_data['balance']}元")
    # 调用数据处理层，保存用户数据
    db_handler.save_data(user_data)

    return True, f"\n{logged_user}充值{money}元成功!\n账户余额为{user_data['balance']}元"


# 提现接口
def withdraw(logged_user, money):
    """
    提现接口
    :param logged_user: 已登录用户
    :param money: 提现金额
    :return: (boolean, str)
    """
    # 获取用户数据
    user_data = db_handler.select_data(logged_user)
    # 计算手续费，并判断余额是否充足
    if money * settings.RATE > user_data["balance"] or money > user_data["balance"]:
        return False, "\n余额不足!"
    # 修改余额
    user_data["balance"] -= (money + money * settings.RATE)
    # 记录流水
    msg = f"\n{datetime.now()}:{logged_user}提现{money}元成功!\n手续费为{money * settings.RATE}元\n账户余额为{user_data['balance']}元"
    user_data["flow"].append(msg)
    # 调用数据处理层，保存用户数据
    db_handler.save_data(user_data)

    return True, msg


# 查询余额接口
def check_balance(logged_user):
    """
    查询余额接口
    :param logged_user: 已登录用户
    :return: (boolean, str)
    """
    # 获取用户数据
    user_data = db_handler.select_data(logged_user)
    return True, f"\n{logged_user}账户余额为{user_data['balance']}元"


# 转账接口
def transfer(logged_user, to_user, money):
    """
    转账接口
    :param logged_user: 已登录用户
    :param to_user: 目标用户
    :param money: 转账金额
    :return: (boolean, str)
    """
    # 获取两个用户的数据
    user_data = db_handler.select_data(logged_user)
    to_user_data = db_handler.select_data(to_user)
    # 判断用户是否存在
    if not to_user_data:
        return False, f"\n用户{to_user}不存在!"
    # 判断用户是否被锁定
    if to_user_data["locked"]:
        return False, f"\n该账号{to_user}已被锁定!"
    # 计算手续费
    fee = money * settings.RATE
    # 判断余额是否充足
    if money + fee > user_data["balance"]:
        return False, "\n余额不足!"
    # 修改余额
    user_data["balance"] -= (money + fee)
    to_user_data["balance"] += money
    # 记录流水
    msg = f"\n{datetime.now()}:{logged_user}向{to_user}转账{money}元成功!\n手续费为{fee}元\n账户余额为{user_data['balance']}元"
    user_data["flow"].append(msg)
    to_msg = f"\n{datetime.now()}:{to_user}收到{logged_user}转账{money}元成功!\n账户余额为{to_user_data['balance']}元"
    to_user_data["flow"].append(to_msg)
    # 调用数据处理层，保存用户数据
    db_handler.save_data(user_data)
    db_handler.save_data(to_user_data)
    return True, msg


# 查看流水接口
def check_flow(logged_user):
    """
    查看流水接口
    :param logged_user: 已登录用户
    :return: (boolean, str)
    """
    # 获取用户数据
    user_data = db_handler.select_data(logged_user)
    return True, user_data["flow"]
