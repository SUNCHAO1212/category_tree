# -*- coding: utf-8 -*-
# !/usr/bin/env python

from __future__ import absolute_import, unicode_literals, print_function

import sys

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import json
import ahocorasick
import codecs
import chardet
import re

ac = ahocorasick.Automaton()

def load_dict():

    # with codecs.open('res/my_dict_event_type.txt', 'rb', 'utf8') as f:
    with codecs.open('res/dict_event_type.txt', 'rb', 'utf8') as f:
        for line in f:
            a=(line.split('\t')[0]).replace('\ufeff','').encode('utf8')
            b=json.loads((line.split('\t')[1]).split('\r')[0])
            ac.add_word(a,b)
    ac.make_automaton()
    f.close()

def judge(title):

    my_dict = {
        'title': title,
        'path': [],
        'idpath': [],
        'choice': []
    }
    id_1=[]
    id_2=[]
    id_3=[]
    idpaths_1=[]
    idpaths_2=[]
    idpaths_3=[]
    idpaths=[]
    idpaths_return=[]
    for item in ac.iter(title.encode('utf8')):
        if item[1]['level']==3:
            id_3.extend(item[1]['id'])
            idpaths_3.extend(item[1]['idpath'])
        elif item[1]['level']==2:
            id_2.extend(item[1]['id'])
            idpaths_2.extend(item[1]['idpath'])
        elif item[1]['level']==1:
            id_1.extend(item[1]['id'])
            idpaths_1.extend(item[1]['idpath'])

    for id1 in id_1:
        idpaths.append(str(id1))
        for id2 in id_2:
            idpaths.append(str(id1)+'/'+str(id2))
            for id3 in id_3:
                idpaths.append(str(id1)+'/' + str(id2)+'/'+str(id3))
    idpaths=list(set(idpaths)&(set(idpaths_1)|set(idpaths_2)|set(idpaths_3)))
    for i in range(0,len(idpaths)):
        for a in range(i,len(idpaths)):
            x=compare(idpaths[i],idpaths[a])
            if x:
                idpaths_return.append(x)
    idpaths_return=set(idpaths_return)
    this_return = list(set(idpaths)-idpaths_return)

    # 记录所有的 path, 并给出当前策略下的选择
    try:
        for id_path in idpaths:
            path_dict = {}
            num_list = id_path.split('/')
            list_len = len(num_list)
            for i in range(0, list_len):
                for item in ac.iter(title.encode('utf8')):
                    num = int(num_list[i])
                    if num in item[1]['id']:
                        if 0 == i:
                            temp = item[1]['level1'] + ' -> ' + item[1]['level2'] + ' -> ' + item[1]['word']
                            path_dict['level1'] = item[1]['level1']
                            path_dict['level2'] = item[1]['level2']
                            path_dict['level3'] = item[1]['word']
                            print(temp, end='')
                        elif 1 == i:
                            temp = ' -> ' + item[1]['word']
                            path_dict['level4'] = item[1]['word']
                            print(temp, end='')
                        elif 2 == i:
                            temp = ' -> ' + item[1]['word']
                            path_dict['level5'] = item[1]['word']
                            print(temp, end='')
            my_dict['path'].append(path_dict)
            print('')
    except Exception as e:
        fe = open('log_files/error.txt', 'ab')
        fe.write(title + e + '\n')
        fe.close()
        print(e)

    if this_return == []:
        fm = open('log_files/missed.txt', 'ab')
        fm.write(title + '\n')
        fm.close()
        return title + ' No fetch.'
    else:
        my_dict['idpath'] = this_return
        for j in range(0, len(this_return)):
            path_dict = {}
            num_list = this_return[j].split('/')
            list_len = len(num_list)
            for i in range(0, list_len):
                for item in ac.iter(title.encode('utf8')):
                    num = int(num_list[i])
                    if num in item[1]['id']:
                        if 0 == i:
                            temp = item[1]['level1'] + ' -> ' + item[1]['level2'] + ' -> ' + item[1]['word']
                            path_dict['level1'] = item[1]['level1']
                            path_dict['level2'] = item[1]['level2']
                            path_dict['level3'] = item[1]['word']
                            print(temp, end='')
                        elif 1 == i:
                            temp = ' -> ' + item[1]['word']
                            path_dict['level4'] = item[1]['word']
                            print(temp, end='')
                        elif 2 == i:
                            temp = ' -> ' + item[1]['word']
                            path_dict['level5'] = item[1]['word']
                            print(temp, end='')
            my_dict['choice'].append(path_dict)
        print('')
        with open('log_files/result.json', 'ab') as json_file:
            json_file.write(json.dumps(my_dict, ensure_ascii=False) + '\n')
        return this_return

def compare(id1,id2):
    id1s=set(id1.split('/'))
    n1=len(id1s)
    id2s=set(id2.split('/'))
    n2=len(id2s)
    n3=len(id1s|id2s)
    if n3<=n1 or n3<=n2:
        if n1>n2:
            return id2
        elif n1<n2:
            return id1
        else:
            return False
    else:
        return False



def my_tree(title):
    # print(judge('关联交易问询函回复'.encode('utf8')))
    # print(judge('偶发性关联交易评估报告'.encode('utf8')))
    # print(judge('日常关联交易审核意见'.encode('utf8')))
    # print(judge('股票质押解除'.encode('utf8')))
    # print(judge('交易异常波动问询函的回复'.encode('utf8')))
    # print(judge('一二三四五六七'.encode('utf8')))
    print(judge(title.encode('utf8')))


if __name__ == '__main__':
    load_dict()
    with open('log_files/titles.txt') as f:
        for line in f.readlines():
            title = line.strip()
            my_tree(title)
