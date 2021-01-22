import asyncio
import os
import re
import time

import httpx
from configobj import ConfigObj


config = ConfigObj(os.getcwd() + "/config.conf")

sess = httpx.AsyncClient()


async def _login():
    data = {
        'uid': config['Account']['UID'],
        'passwd': config['Account']['PASSWD'],
        'vcode': '7045'
    }

    sess.headers.update(
        {
            'user-agent': 'Bahadroid (https://www.gamer.com.tw/)',
            'x-bahamut-app-instanceid': 'cc2zQIfDpg4',
            'x-bahamut-app-android': 'tw.com.gamer.android.activecenter',
            'x-bahamut-app-version': '251',
            'content-type': 'application/x-www-form-urlencoded',
            'accept-encoding': 'gzip',
            'cookie': 'ckAPP_VCODE=7045'
        },
    )

    account = await sess.post(
        'https://api.gamer.com.tw/mobile_app/user/v3/do_login.php', data=data)
    account_f = account.json()
    print('[Info]Login success!')
    print(f'[Info]您好：{account_f["nickname"]}')
    print('[-----勇者資訊如下-----]')
    print(f'[Info]等級：{account_f["lv"]}')
    print(f'[Info]巴幣：{account_f["gold"]}')
    print(f'[Info]ＧＰ：{account_f["gp"]}')
    sess.headers = {
        'user-agent': 'Bahadroid (https://www.gamer.com.tw/)',
        'x-bahamut-app-instanceid': 'cc2zQIfDpg4',
        'x-bahamut-app-android': 'tw.com.gamer.android.activecenter',
        'x-bahamut-app-version': '251',
        'accept-encoding': 'gzip'}


async def check_lottery():
    while True:
        req = await sess.get('https://fuli.gamer.com.tw/shop.php')
        for _sn in re.findall(r'shop_detail\.php\?sn=(\d*)', req.text):
            req = await sess.get(f'https://fuli.gamer.com.tw/shop_detail.php?sn={_sn}')
            if req.text.find('抽抽樂') != -1 and req.text.find('本日免費兌換次數已用盡') == -1:
                print(f"已將{re.findall(r'<h1>(.*)</h1>', req.text)[0]}新增到抽獎隊列中")
                loop.create_task(lottery(_sn))
            else:
                continue
        await asyncio.sleep(86400)


async def lottery(sn):
    for _ in range(10):
        req = await sess.get(
            f'https://fuli.gamer.com.tw/ajax/check_ad.php?area=item&sn={sn}')
        await asyncio.sleep(30)
        req = await sess.get(
            f'https://fuli.gamer.com.tw/ajax/getCSRFToken.php?_={int(time.time()*1000)}')
        finish_ad = {
            'token': req.text,
            'area': 'item',
            'sn': sn
        }
        req = await sess.post(
            'https://fuli.gamer.com.tw/ajax/finish_ad.php', data=finish_ad)
        req = await sess.get(f'https://fuli.gamer.com.tw/buyD.php?ad=1&sn={sn}')
        try:
            token = re.findall(r'token.*"(.*)">', req.text)[0]
        except IndexError:
            print('可能有需要回答問題')
            break
        buy = {
            'ticket': '1',
            'name': config['Lottery']['name'],
            'tel': config['Lottery']['tel'],
            'zip': config['Lottery']['zipcode'],
            'city': config['Lottery']['city'],
            'country': config['Lottery']['country'],
            'address': config['Lottery']['address'],
            'recordUserInfo': '1',
            'agreeConfirm': '1',
            'sn': sn,
            'token': token,
            'ad': '1'
        }
        req = await sess.post(
            'https://fuli.gamer.com.tw/buyD_action.php', data=buy)
        await asyncio.sleep(60 * 30 + 10)


loop = asyncio.get_event_loop()
loop.run_until_complete(_login())
loop.create_task(check_lottery())
loop.run_forever()
