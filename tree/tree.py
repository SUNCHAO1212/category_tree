# -*- coding: utf-8 -*-
# !/usr/bin/env python

from __future__ import absolute_import, unicode_literals, print_function

import sys
import MySQLdb
import codecs
from datetime import datetime

try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

conn = MySQLdb.connect(host="192.168.1.252", user="root", passwd="123456", db="guojiandb", charset="utf8")
cursor = conn.cursor()


# update and insert
def insert2mysql(table_name, item):
    qmarks = ', '.join(['%s'] * len(item))  # 用于替换记录值
    cols = ', '.join(item.keys())  # 字段名
    sql = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, cols, qmarks)
    try:
        cursor.execute(sql, item.values())
    except Exception as e:
        print(e)

        update_v = ','.join(['%s="%s"' % (k, v) for k, v in zip(item.keys(), item.values()) if k != 'unique_md5'])

        sql = 'UPDATE %s set %s where unique_md5="%s"' % (table_name, update_v, item['unique_md5'])

        try:
            cursor.execute(sql)
        except Exception as e:
            print(e)

TABLE_PREFIX = 'test_'

# 创建类目库表
def create_new_category_table(tablename):
    create_table_format = """
CREATE TABLE `{}` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `pid` int(11) DEFAULT NULL,
  `category_name` varchar(255) DEFAULT NULL,
  `update_time` datetime DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `idpath` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
"""
    try:
        cursor.execute(create_table_format.format(tablename))
        conn.commit()
    except Exception as e:
        print(e)


# 往类目库表插入数据
def insert_category_table(filepath, tablename, debug=False):
    # 遍历树产生id、pid
    pid_3 = [-1]
    pid_2 = [-1]
    pid_1 = [-1]
    pid_0 = [-1]
    with codecs.open(filepath, 'rb', 'utf8') as f:
        i = 1
        # flag = 1
        for line in f:
            item = {}
            item['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            l = line.strip().split('\t')[0]
            if line.startswith('\t\t\t\t'):
                print('"{}"\t{}\t{}\t{}'.format(l, pid_3[-1], i,
                                                '"{}/{}/{}/{}/{}"'.format(pid_0[-1], pid_1[-1], pid_2[-1], pid_3[-1], i)))
                item['category_name'] = l
                item['pid'] = pid_3[-1]
                item['id'] = i
                item['idpath'] = '{}/{}/{}/{}/{}'.format(pid_0[-1], pid_1[-1], pid_2[-1],pid_3[-1],  i)

                # flag = 3
            elif line.startswith('\t\t\t'):
                pid_3.pop()
                pid_3.append(i)
                print('"{}"\t{}\t{}\t{}'.format(l, pid_2[-1], i,
                                                '"{}/{}/{}/{}"'.format(pid_0[-1], pid_1[-1], pid_2[-1], i)))
                item['category_name'] = l
                item['pid'] = pid_2[-1]
                item['id'] = i
                item['idpath'] = '{}/{}/{}/{}'.format(pid_0[-1], pid_1[-1], pid_2[-1], i)

                # flag = 3
            elif line.startswith('\t\t'):
                pid_2.pop()
                pid_2.append(i)
                print('"{}"\t{}\t{}\t{}'.format(l, pid_1[-1], i, '"{}/{}/{}/{}"'.format(0, pid_0[-1], pid_1[-1], i)))

                item['category_name'] = l
                item['pid'] = pid_1[-1]
                item['id'] = i
                item['idpath'] = '{}/{}/{}'.format(pid_0[-1], pid_1[-1], i)

                # flag = 2
            elif line.startswith('\t'):
                pid_1.pop()
                pid_1.append(i)
                print('"{}"\t{}\t{}\t{}'.format(l, pid_0[-1], i, '"{}/{}/{}"'.format(0, pid_0[-1], i)))

                item['category_name'] = l
                item['pid'] = pid_0[-1]
                item['id'] = i
                item['idpath'] = '{}/{}'.format(pid_0[-1], i)

                # flag = 1
            else:
                pid_0.pop()
                pid_0.append(i)
                print('"{}"\t{}\t{}\t{}'.format(l, 0, i, '"{}/{}"'.format(0, i)))

                item['category_name'] = l
                item['pid'] = 0
                item['id'] = i
                item['idpath'] = '{}'.format( i)
            i += 1

            if not debug:
                insert2mysql(tablename, item)
                conn.commit()

def upsert_catalog_library(tablename, linktablename, groupid=None):
    item = {}
    item['update_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    item['create_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    item['isdel'] = 0
    item['link_tablename'] = TABLE_PREFIX + linktablename
    item['catalog_name'] = linktablename
    item['group_id'] = groupid
    insert2mysql(tablename, item)
    conn.commit()


def new_category(filepath, tablename, debug=False):
    create_new_category_table(TABLE_PREFIX + tablename)
    insert_category_table(filepath, TABLE_PREFIX + tablename, debug)

if __name__ == '__main__':
    new_category('a.txt', 'event_tree')
    # upsert_catalog_library('kb_catalog_library', 'product_liangzhi', 1)
    # new_category('stats_result.txt', 'product_stats')
    # upsert_catalog_library('kb_catalog_library', 'product_stats', 1)
    # new_category('china_area_result.txt', 'area_china')
    # upsert_catalog_library('kb_catalog_library', 'area_china', 2)

    # new_category('ics_result.txt', 'product_ics')
    # upsert_catalog_library('kb_catalog_library', 'product_ics', 1)

    # new_category('shangpinwang.txt', 'product_shangpinwang')
    # upsert_catalog_library('kb_catalog_library', 'product_shangpinwang', 1)

cursor.close()
conn.close()
