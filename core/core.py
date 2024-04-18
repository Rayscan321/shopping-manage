"""
用户视图层
"""
import re
from interface import user_interface, bank_interface, shop_interface
from lib import common

logged_user = None
logged_admin = False


# 0、退出软件
def quit_soft():
    print("\n感谢使用，欢迎下次使用")
    quit()


# 1、注册功能
def register(is_admin=False):
    print("注册功能")
    while True:
        # 用户输入账号密码
        print("\n注册".center(20, "-"))
        username = input("请输入用户名：").strip()
        password = input("请输入密码：").strip()
        re_password = input("请确认密码：").strip()
        is_register = input("按任意键确认|n退出：").strip().lower()

        # 简单的逻辑判断
        # 用户是否想要退出
        if is_register == "n":
            break

        # 两次输入的密码是否一致
        if password != re_password:
            print("\n!两次输入的密码不一致，请重新输入！")
            continue

        # 校验用户名是否合法
        if not re.findall(r"^[a-zA-Z]\w{2,9}$", username):
            print("\n用户名不符合要求！\n用户名必须为3-10个字符，只能由字母、数字、下划线组成，并只能以字母开头")
            continue

        # 校验密码强度
        if not re.findall("^(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9]).{8,16}$", password):
            print("密码强度太弱，必须包含大写字母、小写字母、以及数字，且长度为8到12位")
            continue
        # 密码加密
        password = common.pwd_to_sha256(password)
        # 调用用户接口注册
        status, msg = user_interface.register(username, password, is_admin=is_admin)
        print(msg)
        if status:
            break


# 2、登录功能
def login():
    while True:
        # 用户输入账号密码
        print("\n登录".center(20, "-"))
        username = input("请输入用户名：").strip()
        password = input("请输入密码：").strip()
        is_login = input("按任意键确认|n退出：").strip().lower()
        # 密码加密
        password = common.pwd_to_sha256(password)
        # 简单的逻辑判断
        # 用户是否想要退出
        if is_login == "n":
            break
        # 调用用户接口登录
        status, msg, is_admin = user_interface.login(username, password)
        print(msg)
        if status:
            global logged_user, logged_admin
            logged_user = username
            logged_admin = is_admin
            break


@common.login_auth
# 3、充值功能
def recharge(username=False):
    while True:
        # 用户输入充值金额
        print("\n充值".center(20, "-"))
        money = input("请输入充值金额：").strip()
        is_recharge = input("按任意键确认|n退出：").strip().lower()
        # 简单的逻辑判断
        # 用户是否想要退出
        if is_recharge == "n":
            break
        # 校验充值金额
        if not money.isdigit():
            print("\n充值金额必须为整数")
            continue
        # 充值金额必须大于0
        money = int(money)
        if money <= 0:
            print("\n充值金额必须大于0")
            continue
        # 调用用户接口充值
        if not username:
            username = logged_user
        status, msg = bank_interface.recharge(username, money)
        print(msg)
        if status:
            break


# 4、购物功能
@common.login_auth
def shopping():
    # 初始化购物车
    shopping_cart = {}

    # 调用接口层获取商品数据
    goods = shop_interface.check_product("goods")

    while True:
        # 用户输入购买的商品编号
        print("\n欢迎来到购物".center(20, "-"))
        print(f"{'序号':<10}{'商品编号':<10}{'商品名称':<10}{'商品价格':<10}")
        for index, good in enumerate(goods):
            print(f"{index+1:<10}{good['number']:<10}{good['name']:<10}{good['price']:<10}")
        print("\n24小时服务".center(20, "-"))
        goods_id = input("请输入要购买的商品编号（y结算/n退出）：").strip()
        # 如果good_id为n则调用添加购物车接口，把购物车写入文件
        if goods_id == "n":
            if not shopping_cart:
                break
            status, msg = shop_interface.add_shopping_cart(logged_user, shopping_cart)
            print(msg)
            if status:
                break
        # 如果用户输入y，调用结算接口
        if goods_id == "y":
            if not shopping_cart:
                print("\n购物车为空")
                continue
            status, msg, total_price = shop_interface.close_account(logged_user, shopping_cart)
            print(msg)
            if status:
                print(f"欢迎光临商城".center(20, "-"))
                print("=" * 20)
                print(f"{'序号':<10}{'商品编号':<10}{'商品名称':<10}{'商品价格':<10}{'商品数量':<10}{'商品总价':<10}")
                for index, good in enumerate(shopping_cart.values()):
                    print(
                        f"{index + 1:<10}{good['number']:<10}{good['name']:<10}{good['price']:<10}{good['数量']:<10}{good['数量'] * good['price']:<10}")
                print(f"总价：{total_price}")
                print("=" * 20)
                print(f"欢迎下次光临".center(20, "-"))
                break

        # 判断用户输入的编号是否存在
        if not goods_id.isdigit():
            print("\n请输入正确商品编号")
            continue
        goods_id = int(goods_id)-1
        if goods_id not in list(range(len(goods))):
            print("\n请输入正确商品编号")
            continue

        # 获取用户选择的商品信息
        good_info = goods[goods_id]
        name = good_info["name"]

        # 将商品信息添加到购物车
        # 判断购物车是否存在相同的产品
        if name not in shopping_cart:
            good_info["数量"] = 1
            shopping_cart[name] = good_info
        else:
            shopping_cart[name]["数量"] += 1
        print("\n当前购物车数据".center(20, "-"))
        print(f"{'序号':<10}{'商品编号':<10}{'商品名称':<10}{'商品价格':<10}{'商品数量':<10}{'商品总价':<10}")
        for index, good in enumerate(shopping_cart.values()):
            print(f"{index+1:<10}{good['number']:<10}{good['name']:<10}{good['price']:<10}{good['数量']:<10}{good['数量']*good['price']:<10}")
        # 用户继续购买商品
        # 用户选择结算
        # 用户不想结算，退出购物，将用户购物车数据写入到用户数据


# 5、提现功能
@common.login_auth
def withdraw():
    while True:
        # 用户输入提现金额
        print("\n充值".center(20, "-"))
        money = input("请输入提现金额：").strip()
        is_withdraw = input("按任意键确认|n退出：").strip().lower()
        # 简单的逻辑判断
        # 用户是否想要退出
        if is_withdraw == "n":
            break
        # 校验充值金额
        if not money.isdigit():
            print("\n充值金额必须为整数")
            continue
        # 充值金额必须小于500
        money = int(money)
        if money < 500:
            print("\n充值金额不能小于500")
            continue
        # 调用用户接口充值
        status, msg = bank_interface.withdraw(logged_user, money)
        print(msg)
        if status:
            break


# 6、查看余额
@common.login_auth
def check_balance():
    staus, msg = bank_interface.check_balance(logged_user)
    print(msg)


# 7、查看流水
@common.login_auth
def check_flow():
    status, flow_list = bank_interface.check_flow(logged_user)
    if not flow_list:
        print("\n没有流水记录")
    for flow in flow_list:
        print(flow)


# 8、查看购物车
@common.login_auth
def check_shopping_cart():
    # 调用查看购物车接口
    shop_cart_file = shop_interface.check_shopping_cart(logged_user)
    if not shop_cart_file:
        print("\n购物车空空如也")
        return

    # 打印购物车数据
    print("\n当前购物车数据".center(20, "-"))
    print(f"{'序号':<10}{'商品编号':<10}{'商品名称':<10}{'商品价格':<10}{'商品数量':<10}{'商品总价':<10}")
    for index, good in enumerate(shop_cart_file.values()):
        print(
            f"{index + 1:<10}{good['number']:<10}{good['name']:<10}{good['price']:<10}{good['数量']:<10}{good['数量'] * good['price']:<10}")

        # 让用户选择购买或者退出
        opt = input("y付款/n退出：").strip().lower()
        # 如果用户输入y，就调用结算接口结算
        if opt == "y":
            stauts, msg, total_price = shop_interface.close_account(logged_user, shop_cart_file)
            print(msg)
            if stauts:
                # 调用清空购物车接口
                shop_interface.clear_shop_cart(logged_user)
                # 如果结算失败自动退出查看购物车功能
        break

# 9、退出账号
def logout():
    global logged_user, logged_admin
    print(f"{logged_user}退出账号")
    logged_user = None
    logged_admin = False


# 10、转账功能
@common.login_auth
def transfer():
    while True:
        # 用户输入转账金额
        print("\n转账".center(20, "-"))
        # 接受用户名和转账金额
        to_user = input("请输入对方用户名：").strip()
        money = input("请输入转账金额：").strip()
        is_transfer = input("按任意键确认|n退出：").strip().lower()
        # 简单的逻辑判断
        # 用户是否想要退出
        if is_transfer == "n":
            break
        # 校验转账金额
        if not money.isdigit():
            print("\n充值金额必须为整数")
            continue
        # 转账金额必须大于0
        money = int(money)
        if money <= 0:
            print("\n转账金额必须大于0")
            continue
        # 判断用户是否在为自己转账
        if to_user == logged_user:
            print("\n不能转账给自己")
            continue
        # 调用用户接口充值
        status, msg = bank_interface.transfer(logged_user, to_user, money)
        print(msg)
        if status:
            break


# 11、管理员功能
@common.login_auth
def admin():
    from core import admin
    admin.main()


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
            if logged_admin:
                print(f"{num} {func_dic[num][0]}".center(20, "="))
            else:
                if num != "11":
                    print(f"{num} {func_dic[num][0]}".center(20, "="))
        print("这是底部".center(20, "="))
        choice = input("请选择您需要功能的编号：").strip().lower()
        if choice not in func_dic or (not logged_admin and choice == "11"):
            print("您输入的编号不存在，请重新选择")
            continue
        func = func_dic.get(choice)[1]
        func()


if __name__ == '__main__':
    pass
