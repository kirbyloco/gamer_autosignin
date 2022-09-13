import json
import logging
import os
import platform
import re
import time
import sys

import chromedriver_autoinstaller
import httpx
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

if platform.system() == "Linux":
    from pyvirtualdisplay import Display
    disp = Display()
    disp.start()

FORMAT = '%(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO)
handler = logging.FileHandler('gamer.log', 'a+', 'utf-8')
handler.setFormatter(logging.Formatter(FORMAT))

logging.info('正在初始化')

with open(os.getcwd() + "/config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

chromedriver_autoinstaller.install()
chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
# chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--log-level=3')
chrome_options.add_extension('buster.crx')
driver = webdriver.Chrome(options=chrome_options)

logging.info('等待Chrome初始化完成')

time.sleep(3)

driver.get('https://gamer.com.tw')

sess = httpx.Client()


def login():
    data = {
        'uid': config['account']['username'],
        'passwd': config['account']['password'],
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
    account = sess.post(
        'https://api.gamer.com.tw/mobile_app/user/v3/do_login.php', data=data)
    account_f = account.json()
    if account.status_code != 200:
        logging.error('登入失敗')
        sys.exit(0)
    logging.info('登入成功！')
    logging.info(f'您好：{account_f["nickname"]}')
    # logging.info('[-----勇者資訊如下-----]')
    # logging.info(f'等級：{account_f["lv"]}')
    # logging.info(f'巴幣：{account_f["gold"]}')
    # logging.info(f'GP：{account_f["gp"]}')
    sess.headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    }

    for _key, _value in sess.cookies.items():
        driver.add_cookie(
            {'name': _key, 'value': _value, 'domain': 'gamer.com.tw'})


def check_lottery():
    req = sess.get('https://fuli.gamer.com.tw/shop.php')
    lottery_page = int(re.findall(r'page=(\d)&history=0', req.text)[0])
    for page in range(1, lottery_page + 1):
        req = sess.get(
            f'https://fuli.gamer.com.tw/shop.php?page={page}&history=0')
        for _sn in re.findall(r'shop_detail\.php\?sn=(\d*)', req.text):
            req = sess.get(
                f'https://fuli.gamer.com.tw/shop_detail.php?sn={_sn}')
            if req.text.find('question-popup') == -1:
                answer = []
            else:
                answer = re.findall(
                    r'data-question=\"(\d)\".*data-answer=\"(\d)\"', req.text)
                answer_dict = {}
                for _question, _answer in answer:
                    answer_dict[_question] = _answer
                answer = ' '.join(_ for _ in answer_dict.values())
            title = re.findall(r'<h1>(.*)</h1>', req.text)[0]
            if req.text.find('抽抽樂') != -1 and req.text.find('本日免費兌換次數已用盡') == -1:
                logging.info(f"已將 {title} 新增到抽獎隊列中")
                lottery(_sn, answer, title)


def lottery(sn, answer, title):
    if answer:
        req = sess.get(
            f'https://fuli.gamer.com.tw/ajax/getCSRFToken.php?_={int(time.time()*1000)}')
        data = {
            'sn': sn,
            'token': req.text,
            'answer[]': answer
        }
        req = sess.post(
            'https://fuli.gamer.com.tw/ajax/answer_question.php', data=data)
        logging.debug(req.json())
    for _ in range(1, 11):
        req = sess.get(f'https://fuli.gamer.com.tw/shop_detail.php?sn={sn}')
        if req.text.find('本日免費兌換次數已用盡') != -1:
            logging.warning(f'{title} 已無免費次數')
            break
        logging.info(f'{title} 正在觀看第 {_} 次廣告')
        req = sess.get(
            f'https://fuli.gamer.com.tw/ajax/check_ad.php?area=item&sn={sn}')
        time.sleep(30)
        req = sess.get(
            f'https://fuli.gamer.com.tw/ajax/getCSRFToken.php?_={int(time.time()*1000)}')
        finish_ad = {
            'token': req.text,
            'area': 'item',
            'sn': sn
        }
        req = sess.post(
            'https://fuli.gamer.com.tw/ajax/finish_ad.php', data=finish_ad)
        logging.info(f"{title} 廣告觀看成功")
        driver.get(f'https://fuli.gamer.com.tw/buyD.php?ad=1&sn={sn}')
        driver.find_element(By.ID, "agree-confirm").click()
        driver.find_element(By.CLASS_NAME, "c-primary").click()
        driver.find_element(By.XPATH, '//button[@type="submit"]').click()
        time.sleep(3)
        if driver.find_elements(By.XPATH, '//iframe[@title="recaptcha challenge expires in two minutes"]'):
            driver.switch_to.frame(driver.find_elements(
                By.XPATH, '//iframe[@title="recaptcha challenge expires in two minutes"]')[0])
            if driver.find_elements(By.XPATH, '//div[@class="button-holder help-button-holder"]'):
                driver.find_elements(By.XPATH,
                                     '//div[@class="button-holder help-button-holder"]')[0].click()
        time.sleep(3)
        if driver.current_url.find('message_done') != -1:
            logging.info(f'{title} 廣告抽獎卷成功')
            logging.info(f'{title} 休息30秒')
            time.sleep(30 + 5)
        else:
            logging.error(f'{title} 廣告抽獎卷失敗')
    logging.info(f'完成 {title}')


login()
check_lottery()

driver.quit()
if platform.system() == "Linux":
    disp.stop()
