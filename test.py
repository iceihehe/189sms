# -*- coding=utf-8 -*-
# Created Time: 2015年08月14日 星期五 15时40分54秒
# File Name: test.py

from __future__ import print_function

from basic import AuthCode

app_id = '157548240000244497'
app_secret = 'f05bf9d76cc1c4c3c80606b40b3e284e'

ac = AuthCode(app_id=app_id, app_secret=app_secret)

r = ac.grant_access_token()
access_token = r['access_token']
r = ac.get_token()
token = r['token']
r = ac.send_randcode(token, 'http://weixin.cnlwmy.com/weishequ/', '13808099842')
print(r)
