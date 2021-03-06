#! /usr/bin/env python
#! python3
# coding:utf-8
import re
import requests
import logging
import time
# 配置日志文件和日志级别
logging.basicConfig(filename='SSR-log.log', level=logging.INFO)
logging.getLogger("requests").setLevel(logging.WARNING)

def check(str):
    hasCheckIn = u'<button id="checkin" class="btn btn-success  btn-flat">'
    noChecked = u'<a class="btn btn-success btn-flat disabled" href="#">'
    yes = re.search(hasCheckIn, str)
    if yes is None:
        no = re.search(noChecked, str)
        if no is None:
            return -1  # 什么都没找到
        else:
            return 0  # 找到了“不能签到”
    else:
        return 1  # 找到了“签到”


def match_flows(str):
    res = r'<dl class="dl-horizontal">(.*?)</dl>'
    mm = re.findall(
        res, str, re.S | re.M)
    res = r'<dd>(.*?)</dd>'
    mm = re.findall(
        res, mm[0], re.S | re.M)
    return mm
    # 这段代码是用于解决中文报错的问题


email = 'aa'
password = 'bbb'
loginurl = 'https://ssr.0v0.xyz/auth/login'
# 这行代码，是用来维持cookie的，你后续的操作都不用担心cookie，他会自动带上相应的cookie
s = requests.Session()
# 我们需要带表单的参数
loginparams = {'email': email,'passwd': password, 'remember_me': 'ture'}
# post 数据实现登录
s.post(loginurl, data=loginparams)
# 验证是否登陆成功，抓取首页看看内容
r = s.get(loginurl)
res = check(r.content.decode('utf-8'))  # 0=不能签到;1=可以签到;-1=什么都没找到;
if res == 1:  # 可以签到
    checkinUrl = "https://ssr.0v0.xyz/user/checkin"
    r = s.post(checkinUrl)
    r = s.get(loginurl)
lastFlows = match_flows(r.content.decode('utf-8'))
nowtime = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))  # 获取当前时间
str = '已签到。' + nowtime+',\t总流量：'+lastFlows[0]+',\t已用流量：'+lastFlows[1]+',\t剩余流量：'+lastFlows[2]
print(str)
if res == 1:  # 可以签到
    str2 = '签到成功！' + nowtime + ',\t总流量：'+lastFlows[0]+',\t已用流量：'+lastFlows[1]+',\t剩余流量：'+lastFlows[2]
    logging.info(str2)
