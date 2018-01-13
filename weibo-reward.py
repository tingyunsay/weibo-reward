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
import requests
from pyquery import PyQuery

dcap = dict(DesiredCapabilities.PHANTOMJS)

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

headers_follow = {
    "Accept":"*/*,",
    "Accept-Encoding":"gzip, deflate, br",
    "Accept-Language":"zh-CN,zh;q=0.8",
    "Cache-Control":"no-cache",
    "Connection":"keep-alive",
    "Content-Type":"application/x-www-form-urlencoded",
    #"Cookie":"SINAGLOBAL=6147746042469.108.1500348166534; un=13520235998; UOR=cache.baiducontent.com,widget.weibo.com,login.sina.com.cn; YF-V5-G0=e6f12d86f222067e0079d729f0a701bc; YF-Ugrow-G0=57484c7c1ded49566c905773d5d00f82; WBtopGlobal_register_version=49306022eb5a5f0b; login_sid_t=a94d34bf7e7fc3a10174c50791838383; cross_origin_proto=SSL; _s_tentry=weibo.com; Apache=3176586107803.552.1515847518635; ULV=1515847518642:22:5:5:3176586107803.552.1515847518635:1515781973292; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFFPbxvJMRTSVKvEwZI_yRF5JpX5K2hUgL.Foq7SoMpShefe0n2dJLoIp-LxK-L1K5LB-eLxKBLB.2L1K8kPfYt; ALF=1547383543; SSOLoginState=1515847544; SCF=AmYmQb5ycfnmz1Y0f1jZcZ7EQJiDARpRRPOYTnZBISYT-4-qFIRkh43bYxZwzHA1_gkS4bvjpWH9Z4sv8xy51PE.; SUB=_2A253XY_lDeRhGeBO7VUQ9C3JyDSIHXVUKuYtrDV8PUNbmtANLWbdkW9NRcigXVwBi9C3aciHbnB8Q3rzmBNUtZbD; SUHB=0ElqyoFlimP8mn; wvr=6; YF-Page-G0=59104684d5296c124160a1b451efa4ac; wb_cusLike_6067143538=N",
    "Host":"weibo.com",
    "Origin":"https://weibo.com",
    "Pragma":"no-cache",
    "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "X-Requested-With":"XMLHttpRequest",

}


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

def phantomjs_operator(cookie,url):
    #这里貌似是登录的domain（新浪网的）和微博的domain不一致，导致加cookies有点问题，算了暂时不用了，反正phantomjs也不太稳定
    tingyun_driver = webdriver.PhantomJS(executable_path='/home/node/node_modules/phantomjs-prebuilt/bin/phantomjs')
    tingyun_driver.set_window_size(1124, 850)
    #tingyun_driver.maximize_window()
    #添加cookies的操作：首先需要get一次这个页面，清除cookies之后再添加cookies，这样才能正确地以登录的身份打开这个页面
    tingyun_driver.get(url)
    tingyun_driver.delete_all_cookies()
    cookie['domain'] = '.weibo.com'
    cookie['name'] = 'name'
    cookie['value'] = 'value'
    cookie['path'] = '/'
    #cookie['expiries'] = None#'%s'%str(time.time())
    tingyun_driver.add_cookie(cookie)
    tingyun_driver.get(url)
    time.sleep(2)
    tingyun_driver.save_screenshot("reward.png")
    tingyun_driver.quit()

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
    headers_follow['Referer'] = "https://weibo.com/{uid}/fans?rightmod=1&wvr=6".format(uid=uid)
    res = requests.post(follow_url, cookies=cookie, data=data, headers=headers_follow)
    if res.status_code == 200:
        if res.json()['code'] == "100000":
            logging.info("关注返回成功")
            return True
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



