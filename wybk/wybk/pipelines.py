# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WybkPipeline(object):
    def process_item(self, item, spider):
        return item

import MySQLdb

#同步写入mysql
class MySqlPipeline(object):
    # 初始化
    def __init__(self):
        try:
            self.conn = MySQLdb.connect('127.0.0.1','root','123456','temp', charset='utf8')
            self.cursor = self.conn.cursor()
        except Exception, e:
            print '数据库连接失败'
            print str(e)

    def process_item(self, item, spider):
        print dict(item)
        sql = 'insert into wybk(title,content) ' \
              'values("%s","%s") ' % (item['title'],item['content'])


        print '插入成功'
        try:
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception, e:
            print '插入失败',str(e)
        return item