import sys

import numpy as np
from torch.utils.data import Dataset, DataLoader

from src.sampling import get_word, get_dataset, idx2str


class RumorDataset(Dataset):
    def __init__(self, dataset):
        self.all_data = []
        for data in dataset:
            infos = data.split('\t')
            if len(infos) != 2:
                sys.stderr.write("Error format!")
                continue
            label = []
            label.append(int(infos[1]))
            data = infos[0].split(',')
            data.remove('')
            if len(data) >= 150:
                data = np.array(data[:150]).astype('int64')
            else:
                data = np.concatenate([data, [str(word_dict["<nil>"])] * (150-len(data))]).astype('int64')
            label = np.array(label).astype('int64')
            self.all_data.append((data, label))

    def __getitem__(self, index):
        data, label = self.all_data[index]
        return data, label

    def __len__(self):
        return len(self.all_data)


batch_size = 32
train, test, word_dict = get_dataset()
train_dataset = RumorDataset(train)
test_dataset = RumorDataset(test)
train_loader = DataLoader(train_dataset, shuffle=True, batch_size=batch_size, drop_last=True)
test_loader = DataLoader(test_dataset, shuffle=True, batch_size=batch_size, drop_last=True)
# print('======train dataset======')
# for data, label in train_dataset:
#     print(data)
#     # print(idx2str(data, word_dict))
#     print(np.array(data).shape)
#     print(label)
#
# print('======test dataset======')
# for data, label in test_dataset:
#     print(data)
#     # print(idx2str(data, word_dict))
#     print(np.array(data).shape)
#     print(label)

