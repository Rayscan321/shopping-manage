"""
购物接口
"""
from db import db_handler
from interface import bank_interface
from lib import common

logger = common.get_logger("shopping")


# 查询商品接口
def check_product(goods_filename):
    # 调用数据处理层的查询功能，判断商品是否存在
    product_data = db_handler.select_data(goods_filename, is_user=False)
    return product_data


# 添加购物车接口
def add_shopping_cart(username, shopping_cart):
    # 拿到用户数据里的购物车数据
    user_data = db_handler.select_data(username)
    shopping_cart_file = user_data["shopping_cart"]

    # 添加购物车
    for name in shopping_cart.keys():
        if name in shopping_cart_file:
            shopping_cart_file["name"]["数量"] += shopping_cart["name"]["数量"]
        else:
            shopping_cart_file[name] = shopping_cart[name]

    # 保存用户数据
    db_handler.save_data(user_data)
    msg = f"用户{username}添加购物车成功!"
    logger.info(msg)
    return True, msg


# 结算接口
def close_account(username, shopping_cart):
    # 计算结算总金额
    total_price = 0
    for good_info in shopping_cart.values():
        price = good_info["price"]
        count = good_info["数量"]
        total_price += (price * count)

    stauts, msg = bank_interface.pay(username, total_price)
    return stauts, msg, total_price


# 查看购物车接口
def check_shopping_cart(username):
    user_data = db_handler.select_data(username)
    shopping_cart_file = user_data["shopping_cart"]
    msg = f"用户{username}查看了购物车"
    logger.info(msg)
    return shopping_cart_file

# 清空购物车接口
def clear_shop_cart(username):
    user_data = db_handler.select_data(username)
    user_data["shopping_cart"] = {}
    db_handler.save_data(user_data)