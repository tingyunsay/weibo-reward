#!/usr/bin/env python
# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from selenium import webdriver
import logging
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import re
import json
import base64
import random
import datetime
import requests
import pymysql
from pyquery import PyQuery

file_name = __file__.split('/')[-1].replace(".py","")
logging.basicConfig(level=logging.INFO,
                format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='%s.log'%file_name,
                filemode='a')

#将日志打印到标准输出（设定在某个级别之上的错误）
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
console.setFormatter(formatter)
logging.getLogger('').addHandler(console)

dcap = dict(DesiredCapabilities.PHANTOMJS)

comment_list = [
    "转转转，呀呀呀~~[二哈]","抽我抽我~~[二哈]","表白!![二哈]","反正我也中不了[二哈]","咋地啦，还不能中一次呀[二哈]","过年了，求赏点钱回家[二哈]",
    "废话少说，转起来~~[二哈]","杰少我又at你了哦[笑而不语]","[心][心]","[doge][doge]","[坏笑][坏笑]","[喵喵][喵喵]","[笑而不语][笑而不语]",
    "[色][色]","不抽我不理你了[哼][哼]","[爱你][爱你]","求黑幕我[阴险][阴险]","[阴险][阴险]","我就转转看[吃瓜]","求获奖[二哈][二哈]"
]
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

def get_verifycode():
    pass

def weibo_login(login_url,name,pwd):
    login_url = login_url
    user = name
    pwd = pwd
    browser = webdriver.PhantomJS(desired_capabilities=dcap,
                                  executable_path='/home/node/node_modules/phantomjs-prebuilt/bin/phantomjs')
    # 解决无法点击（非button）的事件
    browser.set_window_size(1124, 850)
    # browser = webdriver.Firefox()
    browser.get(login_url)
    time.sleep(1)
    browser.save_screenshot("./png_save/pc_first.png")

    username = browser.find_element_by_name("username")
    username.clear()
    username.send_keys(user)
    browser.save_screenshot("./png_save/pc_user.png")

    password = browser.find_element_by_xpath('//input[@type="password"]')
    password.clear()
    password.send_keys(pwd)
    browser.save_screenshot("./png_save/pc_pass.png")
    """
    #暂时没有密码
    try:
        code = browser.find_element_by_name("captcha")
        code.clear()
        img = browser.find_element_by_xpath("//div[@class=\"captcha-wrap\"]/img").get_attribute("src")
        img_content = re.sub("data:image/gif;base64,", "", img.encode('utf-8'))
        img_content = base64.b64decode(img_content)
        with open("temp.png", "wb") as f:
            f.write(img_content)
            f.close()
        fuck_code = get_verifycode()
        time.sleep(1)
        code.send_keys(fuck_code)
        # browser.save_screenshot("pc_code.png")
    except Exception, e:
        logging.warning(e)
        logging.warning("没有验证码.....")
        pass
    """
    commit = browser.find_element_by_xpath('//input[@type="submit"]')
    commit.click()
    time.sleep(5)
    browser.save_screenshot("./png_save/fuck_ok.png")

    cookie = {}
    #print browser.title.encode("utf-8")
    if "个人中心" in browser.title.encode('utf-8'):
        for elem in browser.get_cookies():
            cookie[elem["name"]] = elem["value"]
        logging.warning("Get Cookie Success!( Account:%s )" % user)
    print cookie
    return cookie

headers = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding":"gzip, deflate, sdch, br",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Cache-Control":"no-cache",
    "Connection":"keep-alive",
    "Host":"m.weibo.cn",
    "Pragma":"no-cache",
    "Upgrade-Insecure-Requests":"1",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",

}

headers_follow = {
    "Accept":"*/*,",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Cache-Control":"no-cache",
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded",
    "Host":"weibo.com",
    "Origin":"https://weibo.com",
    "Pragma":"no-cache",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest",
}
headers_repost = {
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Cache-Control":"no-cache",
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded",
    "Host":"s.weibo.com",
    "Origin":"http://s.weibo.com",
    "Pragma":"no-cache",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest",
}
headers_dianzan = {
    "Accept":"*/*",
    "Accept-Encoding":"gzip, deflate",
    "Accept-Language":"zh-CN,zh;q=0.9",
    "Cache-Control":"no-cache",
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded",
    "Host":"weibo.com",
    "Origin":"https://weibo.com",
    "Pragma":"no-cache",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/63.0.3239.84 Chrome/63.0.3239.84 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest",
}


def init_database(ip,port,user,password,database="weibo"):
    conn, cursor = db_connetionSS(ip, port, user, password, database)
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
    sql_table = '''CREATE TABLE IF NOT EXISTS tingyun_weibo (
                `mid` varchar(50) NOT NULL,
                `content` text,
                `is_followed` bit(1) NOT NULL,
                `is_reposted` bit(1) NOT NULL,
                `is_dianzan` bit(1) NOT NULL,                
                `topic` varchar(255) DEFAULT NULL,
                `uid` varchar(50) NOT NULL,
                `update_date` datetime DEFAULT NULL,
                PRIMARY KEY (`mid`),
                KEY `uid` (`uid`)
            ) ENGINE=InnoDB CHARSET=utf8'''
    cursor.execute(sql_table)
    conn.commit()
    conn.close()


def follow_someone(uid,cookie):
    follow_url = "https://weibo.com/aj/f/followed?ajwvr=6&__rnd=%s"%(str(int(time.time())) + str(datetime.datetime.now().microsecond/1000))
    data = {
        "uid":uid,
        "objectid":"",
        "f":"1",
        "extra":"",
        "refer_sort":"",
        "refer_flag":"1005050001_",
        "location":"page_100505_home",
        "oid":uid,
        "wforce":"1",
        "nogroup":"false",
        "fnick":"",
        "refer_lflag":"1005050005_",
        "refer_from":"profile_headerv6",
        "_t":"0"
        }
    #headers_follow['Referer'] = "https://weibo.com/{uid}/fans?rightmod=1&wvr=6".format(uid=uid)
    headers_follow['Referer'] = "https://weibo.com/u/{uid}?from=myfollow_all&is_all=1&noscale_head=1".format(uid=uid)
    res = requests.post(follow_url, cookies=cookie, data=data, headers=headers_follow)
    print res.content
    if res.status_code == 200:
        if res.json()['code'] == "100000":
            logging.info("关注返回成功")
            return True
    logging.warning("cookies失效，无法关注他人!")
    return False

def unfollow_someone(uid,cookie):
    unfollow_url = "https://weibo.com/aj/f/unfollow?ajwvr=6"
    data = {
        "uid": uid,
        "objectid": "",
        "f": "1",
        "extra": "",
        "refer_sort": "",
        "refer_flag": "1005050001_",
        "location": "page_100505_home",
        "oid": uid,
        "wforce": "1",
        "nogroup": "false",
        "fnick": "",
        "refer_lflag": "",
        "refer_from": "profile_headerv6",
        "_t": "0"
    }
    headers_follow['Referer'] = "https://weibo.com/u/{uid}?from=myfollow_all&is_all=1".format(uid=uid)
    res = requests.post(unfollow_url, cookies=cookie, data=data, headers=headers_follow)
    if res.status_code == 200:
        if res.json()['code'] == "100000":
            logging.info("取消关注返回成功")
            return True
    logging.warning("cookies失效，无法取消关注!")
    return False

#这里传的是一个message id，即原微博的信息
def repost_weibo(mid,cookie):
    repost_url = "http://s.weibo.com/ajax/mblog/forward?__rnd=%s"%(str(int(time.time())) + str(datetime.datetime.now().microsecond/1000))
    data = {
        "appkey":"",
        "mid":"%s"%mid,
        "style_type":"1",
        "reason":"%s"%random.choice(comment_list),
        "is_comment_base":"1",
        "location":"",
        "_t":"0",
    }
    headers_repost['Referer'] = "http://s.weibo.com/weibo/%25E5%25BE%25AE%25E5%258D%259A%25E6%258A%25BD%25E5%25A5%2596?topnav=1&wvr=6"
    res = requests.post(repost_url, cookies=cookie, data=data, headers=headers_repost)
    if res.status_code == 200:
        if res.json()['code'] == "100000":
            logging.info("抓发微博返回成功")
            return True
    logging.warning("cookies失效，无法转发!")
    return False

#添加一个点赞操作，如果记录失败，稍后重新去点赞，直到三个状态位全部完成
def dianzan_weibo(mid,cookie,uid):
    #这里加个https，我日...
    dianzan_url = "https://weibo.com/aj/v6/like/add?ajwvr=6&__rnd=%s"%(str(int(time.time())) + str(datetime.datetime.now().microsecond/1000))
    data = {
        "location":"page_100505_home",
        "version":"mini",
        "qid":"heart",
        "mid":mid,
        #"loc":"profile",
        #"cuslike":"1",
        "_t":"0",
    }
    #headers_dianzan['Referer'] = "https://weibo.com/u/{uid}?refer_flag=1005055010_&is_hot=1&noscale_head=1".format(uid=uid)
    #headers_dianzan['Cookie'] = json.dumps(cookie)
    headers_dianzan['Referer'] = "https://weibo.com/u/{uid}?profile_ftype=1&is_all=1".format(uid=uid)
    #headers_dianzan['Referer'] = "http://s.weibo.com/weibo/%25E5%25BE%25AE%25E5%258D%259A%25E6%258A%25BD%25E5%25A5%2596?topnav=1&wvr=6&b=1"
    res = requests.post(dianzan_url, cookies=cookie, data=data, headers=headers_dianzan)
    print res.content
    if res.status_code == 200:
        if res.json()['code'] == "100000":
            logging.info("点赞微博返回成功")
            return True
    logging.warning("cookies失效，无法点赞!")
    return False


if __name__ == '__main__':
    user = ""
    pwd = ""
    cookie = weibo_login("https://login.sina.com.cn/signup/signin.php?entry=sso",user,pwd)
    #好多的操作都是基于在自己的账号的uid上操作，先找出来，如果多个账号的话，先登录去自己的主页找出来，再缓存下来使用
    my_uid = "xxxx"
    for i in range(2,3):
        #print str(i)
        #url = "http://s.weibo.com/weibo/%25E5%25BE%25AE%25E5%258D%259A%25E6%258A%25BD%25E5%25A5%2596?topnav=1&wvr=6&b=1&page={page}".format(page=str(i))
        reward_url = "https://m.weibo.cn/api/container/getIndex?type=all&queryVal=%E6%8A%BD%E5%A5%96&featurecode=20000320&luicode=10000011&lfid=106003type%3D1&title=%E6%8A%BD%E5%A5%96&containerid=100103type%3D1%26q%3D%E6%8A%BD%E5%A5%96&page={page}".format(page=i)
        res = requests.get(reward_url,headers=headers).json()#,cookies=cookie)     #这里不需要登录
        if res['ok'] == 1:
            for i in res['data']['cards'][0]['card_group']:
                try:
                    info = {
                        "uid" : i.get('mblog').get('user').get('id'),
                        "name" : i.get('mblog').get('user').get('screen_name'),
                        "text" : i.get('mblog').get('text'),
                    }
                    #这里需要将微博中带有@开头的人都关注上，并且转发的时候带上话题，随机加上一些文字或者图片
                    #明天搞起来，耶耶耶~~
                    print info['text']
                except Exception,e:
                    print e
                    pass



