# -*- coding=utf-8 -*-
# Created Time: 2015年08月14日 星期五 15时16分58秒
# File Name: basic.py

from __future__ import print_function

from datetime import datetime
from hashlib import sha1
import requests
# import json
import hmac
import urllib


class AuthCode(object):
    '''
    短信验证码
    '''
    def __init__(self, *args, **kwargs):
        self._app_id = kwargs.get('app_id')
        self._app_secret = kwargs.get('app_secret')

    def _request(self, method, url, **kwargs):

        r = requests.request(
            method=method,
            url=url,
            **kwargs
        )
        r.raise_for_status()
        response_json = r.json()

        return response_json

    def _get(self, url, **kwargs):
        return self._request(
            method='get',
            url=url,
            **kwargs
        )

    def _post(self, url, **kwargs):
        return self._request(
            method='post',
            url=url,
            **kwargs
        )

    def grant_access_token(
        self, grant_type='client_credentials', state='', scope=''
    ):

        data = {
            'grant_type': grant_type,
            'app_id': self._app_id,
            'app_secret': self._app_secret,
            'state': state,
            'scop': scope,
        }

        return self._post(
            url='https://oauth.api.189.cn/emp/oauth2/v3/access_token',
            data=data,
        )

    def _formatBizQueryParaMap(self, paraMap, urlencode):
        '''格式化参数，签名过程需要使用'''
        slist = sorted(paraMap)
        buff = []
        for k in slist:
            v = urllib.quote(paraMap[k]) if urlencode else paraMap[k]
            buff.append("{0}={1}".format(k, v.encode('utf-8')))
        return "&".join(buff)

    def get_sign(self, key, raw=''):
        if not raw:
            raw = self._app_secret
        signed = hmac.new(raw, key, sha1).digest()\
            .encode('base64').rstrip('\n')
        return signed

    def get_token(self):

        data = {
            'app_id': self._app_id,
            'access_token': self.grant_access_token()['access_token'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        d = self._formatBizQueryParaMap(data, False)
        data.update({
            'sign': self.get_sign(d),
        })

        return self._get(
            url='http://api.189.cn/v2/dm/randcode/token',
            params=data,
        )

    def send_randcode(self, token, url, phone):
        data = {
            'app_id': self._app_id,
            'access_token': self.grant_access_token()['access_token'],
            'token': token,
            'url': url,
            'phone': phone,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }

        d = self._formatBizQueryParaMap(data, False)
        data.update({
            'sign': self.get_sign(d),
        })

        return self._post(
            url='http://api.189.cn/v2/dm/randcode/send',
            data=data,
        )
