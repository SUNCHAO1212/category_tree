# -*- coding:UTF-8 -*-
# !/usr/bin/env python

from __future__ import absolute_import, unicode_literals, print_function

import sys

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import json
import codecs
import re

def make_category():
    #
    f1 = open('res/my_file.txt')
    fo = open('res/my_dict_event_type.txt', 'wb')
    i = 1
    flag = 0
    for line in f1.readlines():
        print(i)
        i += 1
        ######### This method works. The core is encode and decode.
        # obj = re.match(ur'([\u4e00-\u9fa5]+)', line.strip().decode('utf8'))
        # print(obj.group(1))
        u1, u2 = line.strip().decode('utf8').split('\t')
        # print(u1)
        # print(u2)
        f2 = open('res/make_category_out.txt')
        for content in f2.readlines():
            dict2 = json.loads(content)
            if dict2.has_key(u1):
                flag = 1
                print(dict2[u1]['level1'] + '\t' + dict2[u1]['level2'] + '\t' + dict2[u1]['word'])
                dict1 = json.loads(u2)
                # print(dict1['category'] + '\t' + dict1['idpath'] + '\t' + dict1['id'] + '\t' + dict1['level'])
                if dict1['level'] == 1:
                    my_dict = {
                        'category': dict1['category'],
                        'idpath': dict1['idpath'],
                        'id': dict1['id'],
                        'level': dict1['level'],
                        'level1': dict2[u1]['level1'],
                        'level2': dict2[u1]['level2'],
                        'word': dict2[u1]['word']
                    }
                    my_str = json.dumps(my_dict)
                    fo.write(u1 + '\t' + my_str + '\n')
                else:
                    my_dict = {
                        'category': dict1['category'],
                        'idpath': dict1['idpath'],
                        'id': dict1['id'],
                        'level': dict1['level'],
                        'level1': dict2[u1]['level1'],
                        'level2': dict2[u1]['level2'],
                        'word': dict2[u1]['word']
                    }
                    my_str = json.dumps(my_dict)
                    fo.write(u1 + '\t' + my_str + '\n')
            else:

                pass
        f2.close()
        if flag == 0:
            fo.write(line)
        elif flag == 1:
            flag = 0
        # break
    f1.close()
    fo.close()


def make_dict():
    f2 = open('res/make_category.txt')
    fo = open('res/make_category_out.txt', 'wb')
    for line in f2.readlines():
        i = 1
        for word in line.strip().split('\t'):
            if 1 == i:
                level1 = word
            elif 2 == i:
                level2 = word
            else:
                word_dict = {
                    'level1': level1,
                    'level2': level2,
                    'word': word
                }
                my_dict = {unicode(word): word_dict}
                my_str = json.dumps(my_dict)
                # my_str = json.dumps(word_dict)
                fo.write(my_str + '\n')
            i += 1
        # break
    f2.close()
    fo.close()

def test_dict():
    f = open('res/make_category_out.txt')
    for line in f.readlines():
        # print(line)
        my_dict = json.loads(line.strip())
        print(my_dict['短期融资券']['level1'])
        print(my_dict['短期融资券']['level2'])
        print(my_dict['短期融资券']['word'])
        break
    f.close()



if __name__ == '__main__':
    # make_category()
    make_dict()
    # test_dict()
