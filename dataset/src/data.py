# 用于处理数据集

import os

def read_dataset():
    rumor_dir = os.listdir("../CED_Dataset/rumor-repost")
    non_rumor_dir = os.listdir("../CED_Dataset/non-rumor-repost")
    rumor_num = len(rumor_dir)
    non_rumor_num = len(non_rumor_dir)
    print(f"谣言数量为{rumor_num}")
    print(f"非谣言数量为{non_rumor_num}")

read_dataset()