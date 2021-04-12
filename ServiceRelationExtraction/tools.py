import json
import numpy as np
from random import choice
from tqdm import tqdm
import model
import torch
from torch.autograd import Variable
import os
import torch.utils.data as Data
import torch.nn.functional as F

import time

torch.backends.cudnn.benchmark = True

dev_data = json.load(open('./dev_data_me.json'))
id2predicate, predicate2id = json.load(open('./all_50_schemas_me.json'))
id2predicate = {int(i): j for i, j in id2predicate.items()}
id2char, char2id = json.load(open('./all_chars_me.json'))
num_classes = len(id2predicate)

s_m = torch.load("./models/s_32.pkl",map_location='cpu')
po_m = torch.load("./models/po_32.pkl",map_location='cpu')

s_m = s_m.eval()
po_m = po_m.eval()

def extract_items(text_in):
    R = []
    _s = [char2id.get(c, 1) for c in text_in]
    _s = np.array([_s])
    _k1, _k2, t, t_max, mask = s_m(torch.LongTensor(_s))
    _k1, _k2 = _k1[0, :, 0], _k2[0, :, 0]
    _kk1s = []
    for i, _kk1 in enumerate(_k1):
        if _kk1 > 0.5:
            _subject = ''
            for j, _kk2 in enumerate(_k2[i:]):
                if _kk2 > 0.5:
                    _subject = text_in[i: i + j + 1]
                    break
            if _subject:
                _k1, _k2 = torch.LongTensor([[i]]), torch.LongTensor([[i + j]])  # np.array([i]), np.array([i+j])
                _o1, _o2 = po_m(t, t_max, _k1, _k2)
                _o1, _o2 = _o1.cpu().data.numpy(), _o2.cpu().data.numpy()

                _o1, _o2 = np.argmax(_o1[0], 1), np.argmax(_o2[0], 1)

                for i, _oo1 in enumerate(_o1):
                    if _oo1 > 0:
                        for j, _oo2 in enumerate(_o2[i:]):
                            if _oo2 == _oo1:
                                _object = text_in[i: i + j + 1]
                                _predicate = id2predicate[_oo1]
                                # print((_subject, _predicate, _object))
                                R.append((_subject, _predicate, _object))
                                break
        _kk1s.append(_kk1.data.cpu().numpy())
    _kk1s = np.array(_kk1s)
    return list(set(R))
if __name__=="__main__":
    print(time.time())
    print(extract_items("《岁月如歌》是TVB台庆剧《冲上云霄》的主题曲，是香港歌手陈奕迅演唱的歌曲，由徐伟贤作曲，刘卓辉作词，刘志远编曲，收录于2003年7月22日发行的粤语专辑《Live For Today》中，国语版《兄妹》收录于2003年4月1日发行的专辑《黑·白·灰》中"))
    print(time.time())
    print(extract_items(dev_data[319]['text']))
    print(time.time())
    print(extract_items(dev_data[530]['text']))
    print(time.time())
    print(extract_items(dev_data[812]['text']))
