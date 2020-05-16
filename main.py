import requests
import os
from configobj import ConfigObj

config = ConfigObj(os.getcwd() + "/config.conf")['Account']


def _autosign(baseLogin):
    token = baseLogin.get(
        'https://www.gamer.com.tw/ajax/get_csrf_token.php').text
    jsoninfo = baseLogin.post(
        'https://www.gamer.com.tw/ajax/signin.php', data={'action': '1', 'token': token})
    jsoninfo2 = baseLogin.post(
        'https://www.gamer.com.tw/ajax/signin.php', data={'action': '2'})
    jsoninfo = jsoninfo.json()
    jsoninfo2 = jsoninfo2.json()
    print(token)
    if jsoninfo['message'] == '簽到成功':
        print(f'簽到成功，已簽到 {str(jsoninfo2["days"])} 天')


def _login(data):
    baseLogin = requests.session()
    baseLogin.headers.update(
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

    account = baseLogin.post(
        'https://api.gamer.com.tw/mobile_app/user/v3/do_login.php', data=data)
    account_f = account.json()
    baseLogin.headers = {
        'user-agent': 'Bahadroid (https://www.gamer.com.tw/)',
        'x-bahamut-app-instanceid': 'cc2zQIfDpg4',
        'x-bahamut-app-android': 'tw.com.gamer.android.activecenter',
        'x-bahamut-app-version': '251',
        'accept-encoding': 'gzip'
    }
    _autosign(baseLogin)


if __name__ == "__main__":
    data = {
        'uid': config['UID'],
        'passwd': config['PASSWD'],
        'vcode': '7045'
    }
    _login(data)
