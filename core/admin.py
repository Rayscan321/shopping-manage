"""
管理员视图层
"""
import core
from interface import admin_interface


# 添加账户功能
def add_user():
    is_admin = input("是否要添加管理员账户（y/n）：").strip().lower()
    if is_admin == "y":
        core.register(True)


# 冻结账户功能
def lock_user():
    while True:
        locked_username = input("请输入要冻结账户的用户名：").strip()
        is_lock = input("是否要冻结账户（y/n）：").strip().lower()
        # 判断是否想要退出
        if is_lock == "n":
            break
        # 调用管理员接口冻结账户
        status, msg = admin_interface.lock_user(locked_username)
        print(msg)
        if status:
            break


# 给用户充值
def recharge_to_user():
    user_name = input("请输入要给用户充值的用户名：").strip()
    core.recharge(user_name)


func_dic = {
    "0": ("返回首页", ),
    "1": ("添加账户", add_user),
    "2": ("冻结账户", lock_user),
    "3": ("给用户充值", recharge_to_user),
}


# 管理员视图层主程序
def main():
    while True:
        print("管理员功能".center(20, "="))
        for num in func_dic:
            print(f"{num} {func_dic[num][0]}".center(20, "="))
        print("这是底部".center(20, "="))
        choice = input("请选择您需要功能的编号：").strip().lower()
        if choice == "0":
            break
        if choice in func_dic:
            func = func_dic.get(choice)[1]
            func()
        else:
            print("您输入的编号不存在，请重新选择")
