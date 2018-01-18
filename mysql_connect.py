#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import pymysql
import logging

config = {
    "ip":"127.0.0.1",
    "port":3306,
    "user":"root",
    "pwd":"liaohong",
    "db":"weibo",
    "table":"tingyun_weibo"
}


def escape(string):
    return '`%s`' % string

placeholder = '%s'

def db_connetionSS(ip,port,user,pwd,db):
    conn = pymysql.connect(host=ip,
                           port=port,
                           user=user,
                           password=pwd,
                           db=db,
                           charset='utf8'
                           )
    cursor = pymysql.cursors.SSCursor(conn)
    return conn,cursor

def init_database():
    conn, cursor = db_connetionSS(config['ip'], config['port'], config['user'], config['pwd'], config['db'])
    database = config['db']
    cursor.execute("show databases;")
    databases = [x[0] for x in cursor.fetchall()]
    if database not in databases:
        sql_database = "create database if not exists %s"%database
        cursor.execute(sql_database)
        conn.commit()
        logging.info("数据库 %s 建立完成."%database)
    logging.info("数据库 %s 已经存在." % database)
    #这里我们默认是走：
    # 1.关注微博中提到的所有人（微博抽检平台已关注，会被跳过）
    # 2.at3个好友
    # 3.评论+转发
    #所以，字段只需要：是否关注，是否转发+评论（这两个是放到一起的，一个接口同时做两件事情）
    #以上两者都完成了，这样才是完成的，查库的时候只需要按照条件查询即可
    sql_table = '''CREATE TABLE IF NOT EXISTS %s (
                `id` bigint NOT NULL auto_increment unique key,
                `mid` varchar(50) NOT NULL,
                `name` varchar(50) NOT NULL,
                `content` text,                
                `topic` varchar(255) DEFAULT NULL,
                `uid` varchar(50) NOT NULL,
                `url` varchar(1024) NOT NULL,
                `is_followed` varchar(2) NOT NULL,
                `is_reposted` varchar(2) NOT NULL,
                `is_dianzan` varchar(2) NOT NULL,
                `update_date` datetime DEFAULT NULL,
                PRIMARY KEY (`mid`),
                KEY `uid` (`uid`)
            ) ENGINE=InnoDB CHARSET=utf8'''%(config['table'])
    cursor.execute(sql_table)
    conn.commit()
    conn.close()

#插入数据，接收json的格式去解析
def insert_mysql(data):
    conn, cursor = db_connetionSS(config['ip'], config['port'], config['user'], config['pwd'], config['db'])
    sql = "insert into {table}".format(table=config['table'])
    if isinstance(data,dict):
        try:
            _keys = ", ".join((escape(k) for k in data.keys()))
            #_values = ", ".join([placeholder, ] * len(data))
            _values = ", ".join(("'%s'"%v for v in data.values()))
            sql_query = "INSERT INTO %s (%s) VALUES (%s)" % (config['table'], _keys, _values)
            cursor.execute(sql_query)
            conn.commit()
            conn.close()
        except Exception,e:
            logging.warning(e)
            logging.warning("插入数据失败，请检查语句: {sql}".format(sql=sql_query))
            return False
    logging.info("插入一条数据成功")
    return True

#查询mid是否存在，存在即不再重复插入信息
def select_exists(mid):
    conn, cursor = db_connetionSS(config['ip'], config['port'], config['user'], config['pwd'], config['db'])
    sql = "select count(1) from %s where mid = '%s'"%(config['table'],mid)
    cursor.execute(sql)
    res = cursor.fetchall()
    conn.close()
    #查出来的记录就一条，count(1)
    if res[0][0]:
        return True
    return False
if __name__ == '__main__':
    init_database()
    #select_exists("1")
    data = {
        "mid" : "1",
        "name" : "2",
        "content" : "3",
        "topic": "4",
        "uid" : "5",
        "url" : "6",
        "is_followed": "1",
    }
    if select_exists("1"):
        logging.warning("mid 已经存在，丢弃")
    else:
        insert_mysql(data)
