# 用于处理数据集
import json
import os
import random

import numpy as np

non_rumor_label = "1"
rumor_label = "0"


def read_dataset():
    # read dataset
    rumor_list = os.listdir("../CED_Dataset/rumor-repost")
    non_rumor_list = os.listdir("../CED_Dataset/non-rumor-repost")
    original_microblog = "../CED_Dataset/original-microblog/"
    rumor_num = len(rumor_list)
    non_rumor_num = len(non_rumor_list)
    print(f"谣言数量为{rumor_num}")
    print(f"非谣言数量为{non_rumor_num}")

    # decode json
    # for rumor list
    rumor_info_list = []
    for rumor_single in rumor_list:
        with open(original_microblog + rumor_single, 'r', encoding='utf-8', errors='ignore') as f:
            rumor_info = f.read()
        try:
            rumor_dict = json.loads(rumor_info)
            rumor_info_list.append(rumor_label + '\t' + rumor_dict['text'])
        except json.JSONDecodeError as e:
            print(f"Error decode file {rumor_single}, "
                  f"error is {e}, "
                  f"and the content is {rumor_info}")

    # for non rumor list
    non_rumor_info_list = []
    for non_rumor_single in non_rumor_list:
        with open(original_microblog + non_rumor_single, 'r', encoding='utf-8', errors='ignore') as f:
            non_rumor_info = f.read()
        try:
            non_rumor_dict = json.loads(non_rumor_info)
            non_rumor_info_list.append(non_rumor_label + '\t' + non_rumor_dict['text'])
        except json.JSONDecodeError as e:
            print(f"Error decode file {non_rumor_single}, "
                  f"error is {e}, "
                  f"and the content is {non_rumor_info}")

    # for total rumor list
    total_info_list = non_rumor_info_list + rumor_info_list

    return rumor_info_list, non_rumor_info_list, total_info_list


def print_list(info_list):
    for info in info_list:
        print(info + "\n")


def create_dict(total_info_list):
    # delete the repeated words
    word_set = set()
    for info in total_info_list:
        for ch in info:
            word_set.add(ch)
    word_set.add("<unknown>")
    word_set.add("<nil>")

    # generate word dict
    word_dict = dict()
    i = 0
    for word in word_set:
        word_dict.update({word: i})
        i += 1
    return word_dict


def data_split(rumor_info_list, non_rumor_info_list):
    train_ratio = 0.8
    rumor_num = len(rumor_info_list)
    non_rumor_num = len(non_rumor_info_list)
    train_rumor_num = int(train_ratio * rumor_num)
    train_non_rumor_num = int(train_ratio * non_rumor_num)

    rumor_idx = list(range(rumor_num))
    non_rumor_idx = list(range(non_rumor_num))

    train_rumor_idx = random.sample(rumor_idx, train_rumor_num)
    train_rumor_list = [rumor_info_list[idx] for idx in rumor_idx if idx in train_rumor_idx]
    test_rumor_list = [rumor_info_list[idx] for idx in rumor_idx if idx not in train_rumor_idx]
    train_non_rumor_idx = random.sample(non_rumor_idx, train_non_rumor_num)
    train_non_rumor_list = [non_rumor_info_list[idx] for idx in non_rumor_idx if idx in train_non_rumor_idx]
    test_non_rumor_list = [non_rumor_info_list[idx] for idx in non_rumor_idx if idx not in train_non_rumor_idx]

    # print(len(train_rumor_list), len(test_rumor_list), len(train_non_rumor_list), len(test_non_rumor_list))
    return train_rumor_list, test_rumor_list, train_non_rumor_list, test_non_rumor_list

def sum_up(dataset_1, dataset_2, dict):
    tmp_dataset = dataset_1 + dataset_2
    new_dataset = []

    maxlen = 0
    check = True
    for info in tmp_dataset:
        info_str = ""
        words = info.split('\t')[-1]
        maxlen = max(maxlen, len(words))
        label = info.split('\t')[0]
        for ch in words:
            info_ch = str(dict[ch])
            info_str = info_str + info_ch + ','
        info_str = info_str + '\t' + label
        new_dataset.append(info_str)
    print(f"Successfully generate length {maxlen}")
    return new_dataset

def get_dataset():
    rumor_info_list, non_rumor_info_list, total_info_list = read_dataset()
    word_dict = create_dict(total_info_list)
    train_rumor_list, test_rumor_list, train_non_rumor_list, test_non_rumor_list = data_split(rumor_info_list, non_rumor_info_list)
    train_dataset = sum_up(train_rumor_list, train_non_rumor_list, word_dict)
    test_dataset = sum_up(test_non_rumor_list, test_rumor_list, word_dict)
    random.shuffle(train_dataset)
    random.shuffle(test_dataset)
    return train_dataset, test_dataset, word_dict

def get_word(num, word_dict):
    for key, value in word_dict.items():
        if value == num:
            return key

def idx2str(data_list, word_dict):
    context = ""
    for data in data_list:
        if data != '':
            context += get_word(int(data), word_dict)
        else:
            data.remove(data)

    print(f"the word is {context}")
    print("-----------------------")




# train_dataset, test_dataset, word_dict = get_dataset()
# idx2str()

