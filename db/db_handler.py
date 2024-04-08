"""
数据处理层
"""
import json
import os
from conf import settings


# 查询数据
def select_data(username, data=True, is_user=True):
    if is_user:
        # 接受逻辑接口层的username，并拼出用户名.json的路径
        user_path = os.path.join(
            settings.USER_DATA_DIR, f"{username}.json"
        )
    else:
        user_path = os.path.join(
            settings.GOODS_DATA_DIR, f"{username}.json"
        )

    # 查看用户名是否存在
    if not os.path.exists(user_path):
        return
    # 判断是否需要传回数据，如果不需要传回数据，直接返回True
    if not data:
        return True
    # 需要则读取用户数据，并返回用户数据
    with open(user_path, "rt", encoding="utf-8-sig") as f:
        user_data = json.load(f)
        return user_data


# 保存数据
def save_data(user_data):
    # 接受逻辑接口层的user_data，拼出用户名.json的路径
    user_path = os.path.join(
        settings.USER_DATA_DIR, f"{user_data['username']}.json"
    )
    # 保存用户数据
    with open(user_path, "wt", encoding="utf-8") as f:
        json.dump(user_data, f, ensure_ascii=False)
