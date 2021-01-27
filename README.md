# 巴哈姆特自動簽到

登入程式碼參考
[XinBow99/BAHA_POSTER_Python](https://github.com/XinBow99/BAHA_POSTER_Python "XinBow99/BAHA_POSTER_Python")

## Linux排程
建議不要再00:00的時候執行，避免網路延遲導致無法簽到

自動回答問題是透過blackXblue小屋的答案回答，

所以排程建議設在00:10之後
```
10 0 * * * python3 <your path>/main.py > /dev/null 2>&1
```

## 抽勇者福利社(廣告)
請使用screen或systemd等工具在背景執行

## 已加入的功能
自動簽到 2019-11-14

自動回答動畫瘋的問題 2020-11-24 新增

自動公會簽到 2020-12-06 新增

自動抽勇者福利社的獎品(廣告) 2021-01-22 新增

## config檔設定
使用記事本等工具打開，並填入相關的資料

|Account|登入用|
|-|-|
|UID|使用者帳號|
|PASSWD|密碼|

|Lottery|抽獎用|
|-|-|
|name|真實姓名|
|tel|手機電話|
|zip|郵遞區號|
|city|城市|
|country|鄉鎮區|
|address|地址|

## 待加入的功能
自動回答勇者福利社的問題
