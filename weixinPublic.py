#-*- coding:utf-8 -*-
import requests
import json
import time

USERNAME = ''
PASSWORD = ''


LOGIN_URL = 'https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN'
SEND_URL = 'https://mp.weixin.qq.com/cgi-bin/singlesend'
MESSAGE_URL = 'https://mp.weixin.qq.com/cgi-bin/message'


def login():
    payload = {
            'username': USERNAME, 
            'pwd': md5(PASSWORD[0:16]),
            'imgcode': '',
            'f': 'json'
            }
    header = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'mp.weixin.qq.com',
            'Origin': 'https://mp.weixin.qq.com',
            'Referer': 'https://mp.weixin.qq.com/',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36',
            'X-Requested_With': 'XMLHttpRequest'
            }
    r = requests.post(LOGIN_URL, data=payload, headers=header)
    token = json.loads(r.text)['ErrMsg'].split('&')[-1][6:]
    header['Cookie'] = parse_cookie(r.headers['set-cookie'])
    header['Referer'] = 'https://mp.weixin.qq.com/cgi-bin/message?t=message/list&count=20&day=7&lang=zh_CN'
    #userId = bindUserId(token, header, content)
    #send(userId, token, header, '喝喝水哦')
    return

def bindUserId(token, header, content):
    data = {
            'token': token,
            'lang': 'zh_CN',
            'count': 40,
            'day': 7,
            't': 'message/list'
            }
    r = requests.get(MESSAGE_URL, params=data, headers=header)
    content = r.content
    begin = content.find('list')
    begin = content.find('msg_item', begin)
    end = content.find('msg_item', begin + 1)
    messages = content[begin + 11 : end - 4]
    for message in messages.replace(',"refuse_reason":""},', '}$$$').split("$$$"):
        obj = json.loads(message)
        #get the read Id of User after knowing what it send to you
        if obj['content'] == content: 
            return obj['fakeid']
    return None;

def send(people, token, header, content):
    data = {
            'mask': False,
            'tofakeid': people,
            'imgcode': '',
            'type': 1,
            'content': content,
            #'content': 'send from python' + time.strftime('%Y-%m-%d %X', time.localtime()),
            'lang': 'zh_CN',
            'token': token,
            't': 'ajax-response'
            }
    r = requests.post(SEND_URL, data=data, headers=header)
    return

def save_cookie():
    return

def md5(origin):
    import hashlib
    m = hashlib.md5()
    m.update(origin)
    return m.hexdigest()

def parse_cookie(raw_cookies):
    auth = [] 
    for cookie in raw_cookies.split(';'):
        for a in cookie.split(','):
            if(a[0:5] == 'cert=' or a[0:11] == ' slave_user' or a[0:10] == ' slave_sid'):
                auth.append(a)
    return (';').join(auth)

