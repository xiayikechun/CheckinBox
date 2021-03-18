# -*- coding: utf8 -*-

import requests, os
from bs4 import BeautifulSoup

cookie = os.environ.get('cookie_52pj')

def pusher(*args):
    msg = args[0]
    othermsg = ""
    for i in range(1, len(args)):
        othermsg += args[i]
        othermsg += "\n"
    ID = os.environ.get('ID') # 企业微信id
    AGENTLDS = os.environ.get('AGENTLDS') # 应用id
    SECRET = os.environ.get('SECRET') # 应用密码
    
    if ID:
        #企业微信通知，普通微信可接收

        #获得access_token
        sendurl = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken'
        token_param = '?corpid=' + {ID} + '&corpsecret=' + {SECRET}
        token_data = requests.get(url + token_param)
        token_data.encoding = 'utf-8'
        token_data = token_data.json()
        access_token = token_data['access_token']
        #发送内容
        content = readFile_text('msg,othermsg')
        #创建要发送的消息
        data = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": {AGENTLDS},
            "text": {"content": content}
               }
        send_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=' + access_token
        message = requests.post(send_url,json=data)
        message.encoding = 'utf-8'
        res = message.json()
        print('Wechat send : ' + res['errmsg'])
    
    
        requests.post(sendurl, data=data)
    if SCTKEY:
        sendurl = f"https://sctapi.ftqq.com/{SCTKEY}.send"
        data = {
            "title" : msg,
            "desp" : othermsg
            }
        requests.post(sendurl, data=data)


def main(*args):
    try:
        msg = ""
        s = requests.Session()
        headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'Cookie': cookie,
            'ContentType':'text/html;charset=gbk'
        }
        s.get('https://www.52pojie.cn/home.php?mod=task&do=apply&id=2', headers=headers)
        a = s.get('https://www.52pojie.cn/home.php?mod=task&do=draw&id=2', headers=headers)
        b = BeautifulSoup(a.text,'html.parser')
        c = b.find('div',id='messagetext').find('p').text

        if "您需要先登录才能继续本操作"  in c:
            pusher("52pojie  Cookie过期", c)
            print("cookie_52pj失效，需重新获取")
            msg += "cookie_52pj失效，需重新获取"
        elif "恭喜"  in c:
            print("52pj签到成功")
            msg += "52pj签到成功"
        else:
            print(c)
    except:
        if "防护" in b:
            print("触发52pj安全防护，访问出错。自行修改脚本运行时间和次数，总有能访问到的时间")
        # print(b)
        print("52pj出错")
        msg += "52pj出错"
    return msg + "\n"

def pjCheckin(*args):
    msg = ""
    global cookie
    clist = cookie.split("\n")
    i = 0
    while i < len(clist):
        msg += f"第 {i+1} 个账号开始执行任务\n"
        cookie = clist[i]
        msg += main(cookie)
        i += 1
    return msg

if __name__ == "__main__":
    if cookie:
        print("----------52pojie开始尝试签到----------")
        pjCheckin()
        print("----------52pojie签到执行完毕----------")
