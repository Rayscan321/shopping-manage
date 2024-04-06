import os


# 获取项目根路径
BASE_DIR = os.path.dirname(
    os.path.dirname(__file__)
)

# 获取CFG文件路径
CONFIG_PATH = os.path.join(
    BASE_DIR, "settings.cfg"
)

# 获取USER_DATA路径
import configparser
config = configparser.ConfigParser()
config.read(CONFIG_PATH, encoding="utf-8-sig")
USER_DATA_DIR = config.get("path", "USER_DATA_DIR")
if not os.path.exists(USER_DATA_DIR):
    USER_DATA_DIR = os.path.join(
    BASE_DIR, "db", "user_data"
)

if __name__ == "__main__":
    print(USER_DATA_DIR)