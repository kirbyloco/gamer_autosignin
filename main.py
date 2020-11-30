import os
import re
import time

import requests
from configobj import ConfigObj

config = ConfigObj(os.getcwd() + "/config.conf")['Account']


def _autosign(sess):
    signinfo = sess.post('https://www.gamer.com.tw/ajax/signin.php', data={'action': '2'}).json()
    if signinfo['data']['signin'] == 1:
        return
    token = sess.get(
        'https://www.gamer.com.tw/ajax/get_csrf_token.php').text
    jsoninfo = sess.post(
        'https://www.gamer.com.tw/ajax/signin.php', data={'action': '1', 'token': token})
    jsoninfo = jsoninfo.json()
    if 'data' in jsoninfo:
        print(f'巴哈姆特自動簽到成功!!\n已簽到第 {str(jsoninfo["data"]["days"])} 天')
    else:
        print('簽到失敗')
    sess.post('https://api.gamer.com.tw/mobile_app/bahamut/v1/sign_in_ad_start.php')
    time.sleep(30)
    sess.post('https://api.gamer.com.tw/mobile_app/bahamut/v1/sign_in_ad_finished.php')


def _autoanswer(sess):
    snweb = sess.get(
        'https://api.gamer.com.tw/mobile_app/bahamut/v1/home.php?owner=blackXblue&page=1')
    sn = snweb.json()['creation'][0]['sn']
    answeb = sess.get(
        'https://api.gamer.com.tw/mobile_app/bahamut/v1/home_creation_detail.php?sn=' + str(sn))
    ans = re.findall(r"A:(\d)<", answeb.json()['content'])[0]
    tokenweb = sess.get(
        'https://ani.gamer.com.tw/ajax/animeGetQuestion.php?t=' + str(int(time.time() * 1000)))
    token = tokenweb.json()['token']
    data = {
        'token': token,
        'ans': ans,
        't': str(int(time.time() * 1000))
    }
    c = sess.post(
        'https://ani.gamer.com.tw/ajax/animeAnsQuestion.php', data=data)
    jsoninfo = c.json()
    if jsoninfo['ok'] == 1:
        print(jsoninfo['gift'])
    else:
        print('答案錯誤')


def _login(data):
    sess = requests.session()
    sess.headers.update(
        {
            'user-agent': 'Bahadroid (https://www.gamer.com.tw/)',
            'x-bahamut-app-instanceid': 'cc2zQIfDpg4',
            'x-bahamut-app-android': 'tw.com.gamer.android.activecenter',
            'x-bahamut-app-version': '251',
            'content-type': 'application/x-www-form-urlencoded',
            'content-length': '44',
            'accept-encoding': 'gzip',
            'cookie': 'ckAPP_VCODE=7045'
        },
    )

    account = sess.post(
        'https://api.gamer.com.tw/mobile_app/user/v3/do_login.php', data=data)
    account_f = account.json()
    sess.headers = {
        'user-agent': 'Bahadroid (https://www.gamer.com.tw/)',
        'x-bahamut-app-instanceid': 'cc2zQIfDpg4',
        'x-bahamut-app-android': 'tw.com.gamer.android.activecenter',
        'x-bahamut-app-version': '251',
        'accept-encoding': 'gzip'
    }
    _autosign(sess)
    _autoanswer(sess)

if __name__ == "__main__":
    data = {
        'uid': config['UID'],
        'passwd': config['PASSWD'],
        'vcode': '7045'
    }
    _login(data)
