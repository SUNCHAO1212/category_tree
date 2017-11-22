# -*- coding: utf-8 -*-
# !/usr/bin/env python

from __future__ import absolute_import, unicode_literals, print_function

import sys
import MySQLdb
import codecs
from datetime import datetime
import json

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

def test_dict(key):
    # key = key.encode('gb2312')
    print(type(key))
    print(key)
    f = open('make_category_out.txt')
    for line in f.readlines():
        # print(line)
        my_dict = json.loads(line.strip())
        print(my_dict[key]['level1'])
        print(my_dict[key]['level2'])
        print(my_dict[key]['word'])
        break
    f.close()

def make_dict():
    f1 = open('make_category.txt')
    fo = open('make_category_out.txt', 'wb')
    my_dict = {}
    for line in f1.readlines():
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
                my_dict[word] = word_dict
            i += 1
            # break
    my_str = json.dumps(my_dict)
    fo.write(my_str + '\n')
    f1.close()
    fo.close()
    return my_dict

def my_function():
    conn = MySQLdb.connect(host="192.168.1.252", user="root", passwd="123456", db="guojiandb", charset="utf8")
    cursor = conn.cursor()

    dict={}

    f=open('dict_event_type.txt','w')

    sql='SELECT * FROM test_event_tree'
    try:
        cursor.execute(sql)
    except:
        pass



    datas=cursor.fetchall()
    for data in datas:
        argue = {"idpath": [],
                 "level": "",
                 "id": [],
                 # "category": u"股权",
                 "level1": "",
                 "level2": "",
                 "word": "",
                 }
        g=data[2].encode('utf-8')
        if dict.has_key(''+g):
            dict[''+g]['idpath'].append(data[5])
            dict['' + g]['id'].append(data[0])
            dict['' + g]['word'] = g
        else:
            dict['' + g]=argue
            dict[''+g]['idpath'].append(data[5])
            dict[''+g]['level']=len(data[5].split('/'))
            dict['' + g]['id'].append(data[0])
            dict['' + g]['word'] = g

    for k, v in dict.items():
        if my_dict.has_key(k):
            v['level1'] = my_dict[k]['level1']
            v['level2'] = my_dict[k]['level2']
            v['word'] = my_dict[k]['word']

        content = k+'\t'+json.dumps(v)+'\r'
        f.write(content)


if __name__ == '__main__':
    # make_category
    my_dict = make_dict()
    my_function()
