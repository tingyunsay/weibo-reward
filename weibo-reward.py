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
from mysql_connect import *

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

#暂时没有使用到验证码，若需要可接入打码平台
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

#关注他人，uid
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
    #print res.content
    if res.status_code == 200:
        if res.json()['code'] == "100000":
            logging.info("关注返回成功")
            return True
    logging.warning("cookies失效，无法关注他人!")
    return False

#取关这个人，uid
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
def repost_weibo(mid,cookie,topic):
    repost_url = "http://s.weibo.com/ajax/mblog/forward?__rnd=%s"%(str(int(time.time())) + str(datetime.datetime.now().microsecond/1000))
    at_person = ["@白菜君王","@天台球场Killer24","@白菜沙僧"]
    data = {
        "appkey":"",
        "mid":"%s"%mid,
        "style_type":"1",
        "reason":"%s"%random.choice(comment_list)+" ".join(topic)+" ".join(at_person),
        "is_comment_base":"1",
        "location":"",
        "_t":"0",
    }
    headers_repost['Referer'] = "http://s.weibo.com/weibo/%25E5%25BE%25AE%25E5%258D%259A%25E6%258A%25BD%25E5%25A5%2596?topnav=1&wvr=6"
    res = requests.post(repost_url, cookies=cookie, data=data, headers=headers_repost)
    if res.status_code == 200:
        if res.json()['code'] == "100000":
            logging.info("转发微博返回成功")
            return True
    logging.warning("cookies失效，无法转发! 该微博mid为: %s"%mid)
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
    #print res.content
    if res.status_code == 200:
        if res.json()['code'] == "100000":
            logging.info("点赞微博返回成功")
            return True
    logging.warning("cookies失效，无法点赞!")
    return False


if __name__ == '__main__':
    init_database()
    cookie = weibo_login("https://login.sina.com.cn/signup/signin.php?entry=sso","user","pwd")
    #cookie = {u'UOR': u',my.sina.com.cn,', u'SCF': u'Arjt1ViQJ5ggZlcjsyI8cRob_lmZro1DyKYxqLAS1VKjyFJfW_4KKhFGvB-GLGjw8FGxiEow6XzVYwKhgMq7JoM.', u'SUB': u'_2A253W9FXDeRhGeBO7VUQ9C3JyDSIHXVUEUWfrDV_PUNbm9ANLWbjkW9NRcigXaHPnnOB6LVh5aVkpGQ2AviMP38l', u'SUBP': u'0033WrSXqPxfM725Ws9jqgMF55529P9D9WFFPbxvJMRTSVKvEwZI_yRF5NHD95QcehqNeKB0SKeRWs4DqcjHi--fiK.7i-8hi--Xi-iWiK.pPfvk', u'sso_info': u'v02m6alo5qztKWRk5SljpOApZCUjKWRk5ClkKSEpY6ThZ-XtbymnZalpI-TmLCNo5yxjYOMtYyzoMA=', u'ALF': u'1547752516', u'bdshare_firstime': u'1516216517855', u'ULV': u'1516216519120:1:1:1:125.33.204.128_1516216517.743241:', u'WEB2': u'bd9116f57eb1923b3be6331d82475d70', u'ULOGIN_IMG': u'aliyun-ea326361f0d97ccde588c92f21493ff1ce79', u'SINAGLOBAL': u'125.33.204.128_1516216517.743236', u'Apache': u'125.33.204.128_1516216517.743241', u'U_TRS1': u'00000080.7c372c85.5a5fa0c5.42226278', u'U_TRS2': u'00000080.7c3f2c85.5a5fa0c5.1506b0d8'}
    #exit()
    for i in range(2,3):
        #print str(i)
        #url = "http://s.weibo.com/weibo/%25E5%25BE%25AE%25E5%258D%259A%25E6%258A%25BD%25E5%25A5%2596?topnav=1&wvr=6&b=1&page={page}".format(page=str(i))
        reward_url = "https://m.weibo.cn/api/container/getIndex?type=all&queryVal=%E6%8A%BD%E5%A5%96&featurecode=20000320&luicode=10000011&lfid=106003type%3D1&title=%E6%8A%BD%E5%A5%96&containerid=100103type%3D1%26q%3D%E6%8A%BD%E5%A5%96&page={page}".format(page=i)
        res = requests.get(reward_url,headers=headers).json()#,cookies=cookie)     #这里不需要登录
        if res['ok'] == 1:
            for i in res['data']['cards'][0]['card_group']:
                info = {
                    "mid": i.get('mblog').get('mid'),
                    "name": i.get('mblog').get('user').get('screen_name'),
                    "content": PyQuery(i.get('mblog').get('text')).text().replace("'", "\\'"),
                    "topic": json.dumps([str(x).replace("'","\\'") for x in re.findall("#.*?#", i.get('mblog').get('text'))]),
                    "uid": i.get('mblog').get('user').get('id'),
                    "url": i.get('scheme'),
                }
                #print info['topic']
                #continue
                if select_exists(info['mid']):
                    logging.warning("mid {%s} 已经存在，丢弃"%info['mid'])
                else:
                    try:
                        follow_flag = True
                        logging.info("开始关注发微博的人....")
                        try:
                            follow_someone(info['uid'], cookie)
                            logging.info("关注发博人: {%s} 成功" % info['name'])
                        except Exception,e:
                            follow_flag = False
                            logging.warning("关注发博人: {%s} 失败，原因如下:" % info['name'])
                            logging.warning(e)
                            pass
                        #这里需要
                        # 1.将微博中带有@开头的人都关注上
                        # 2.并且转发的时候带上话题，随机加上一些文字或者图片
                        # 3.at三个朋友（一般不会超过三个），yj(319718)，lh(392639),白菜君王(5163218557)
                        #这边只能at用户的名字，然后微博内部自动根据名字的唯一去跳转
                        text_utf8 = info['content'].encode('utf8')
                        if re.findall("微博抽奖平台",text_utf8):
                            logging.info("开始操作一条微博-----------")
                            #设定follow_flag为True，只要下面中关注出现问题即将其置为False（有一个失败即是全部失败）
                            for j in re.findall("(?<=\@).*?(?=<)",text_utf8):
                                if re.search("微博抽奖平台",j):
                                    continue
                                else:
                                    try:
                                        logging.info("开始关注微博中提到的用户 : {%s}"%j)
                                        person_page = "https://m.weibo.cn/n/%s"%j
                                        #print person_page
                                        person_uid = re.findall("\d+$",requests.get(person_page).url)[0]
                                        #print person_uid
                                        #找出了uid，关注它
                                        follow_someone(person_uid,cookie)
                                        logging.info("关注用户 {%s} 成功"%j)
                                    except Exception,e:
                                        follow_flag = False
                                        logging.warning(e)
                                        logging.warning("关注用户 {%s} 出现问题"%j)
                        #只有到这里才全部关注成功
                        info['is_followed'] = 1 if follow_flag else 0

                        dianzan_flag = dianzan_weibo(mid=info['mid'],cookie=cookie,uid=info['uid'])
                        info['is_dianzan'] = 1 if dianzan_flag else 0

                        repost_flag = repost_weibo(mid=info['mid'],cookie=cookie,topic=json.loads(info['topic']))
                        info['is_reposted'] = 1 if repost_flag else 0
                        insert_mysql(info)
                    except Exception,e:
                        print e
                        pass

