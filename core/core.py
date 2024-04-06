"""
用户视图层
"""


# 0、退出软件
def quit_soft():
    print("\n感谢使用，欢迎下次使用")
    quit()


# 1、注册功能
def register():
    print("注册功能")
    while True:
        # 用户输入账号密码
        print("\n注册".center(20, "-"))
        username = input("请输入用户名：").strip()
        password = input("请输入密码：").strip()
        re_password = input("请确认密码：").strip()
        is_register = input("按任意键确认/n退出：").strip().lower()

        # 简单的逻辑判断
        # 用户是否想要退出
        if is_register == "n":
            break

        # 两次输入的密码是否一致
        if password != re_password:
            print("\n!两次输入的密码不一致，请重新输入！")
            continue

        import re
        # 校验用户名是否合法
        if not re.findall(r"^[a-zA-Z]\w{2, 9}$", username):
            print("\n用户名不符合要求！\n用户名必须为3-10个字符，只能由字母、数字、下划线组成，并只能以字母开头")
            continue

        # 校验密码强度
        if not re.findall("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8, 16}$", password):
            print("密码强度太弱，必须包含大写字母、小写字母、以及数字，且长度为8到12位")
            continue


# 2、登录功能
def login():
    print("登录功能")


# 3、充值功能
def recharge():
    print("充值功能")


# 4、购物功能
def shopping():
    print("购物功能")


# 5、提现功能
def withdraw():
    print("提现功能")


# 6、查看余额
def check_balance():
    print("查看余额")


# 7、查看流水
def check_flow():
    print("查看流水")


# 8、查看购物车
def check_shopping_cart():
    print("查看购物车")


# 9、退出账号
def logout():
    print("退出账号")


# 10、转账功能
def transfer():
    print("转账功能")


# 11、管理员功能
def admin():
    print("管理员功能")


func_dic = {
    "0": ("退出软件", quit_soft),
    "1": ("注册功能", register),
    "2": ("登录功能", login),
    "3": ("充值功能", recharge),
    "4": ("购物功能", shopping),
    "5": ("提现功能", withdraw),
    "6": ("查看余额", check_balance),
    "7": ("查看流水", check_flow),
    "8": ("查看购物车", check_shopping_cart),
    "9": ("退出账号", logout),
    "10": ("转账功能", transfer),
    "11": ("管理员功能", admin)
}


# 主程序
def main():
    while True:
        print("购物管理系统".center(20, "="))
        for num in func_dic:
            print(f"{num} {func_dic[num][0]}".center(20, "="))
        print("这是底部".center(20, "="))
        choice = input("请选择您需要功能的编号：").strip().lower()
        if choice in func_dic:
            func = func_dic.get(choice)[1]
            func()
        else:
            print("您输入的编号不存在，请重新选择")


if __name__ == '__main__':
    pass

