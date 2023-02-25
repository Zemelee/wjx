import random

from easydict import EasyDict
import yaml


# 读取配置文件
def cfg_from_yaml_file(cfg_file):
    with open(cfg_file, 'r') as f:
        try:
            config = yaml.safe_load(f, Loader=yaml.FullLoader)
        except:
            config = yaml.safe_load(f)

    return EasyDict(config)


# 生成滑动轨迹
tracks = [i for i in range(1, 21, 3)]


# 生成m到n之间的o个不重复的数字列表
def int_random(m, n, o):
    p = []
    while len(p) < o:
        new_int = random.randint(m, n)
        if new_int not in p:
            p.append(new_int)
    return p

