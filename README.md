# 巴哈姆特自動簽到

登入程式碼參考
[XinBow99/BAHA_POSTER_Python](https://github.com/XinBow99/BAHA_POSTER_Python "XinBow99/BAHA_POSTER_Python")

## Linux排程
建議不要再00:00的時候執行，避免網路延遲導致無法簽到

自動回答問題是透過blackXblue小屋的答案回答，

所以排程建議設在00:10之後
```
10 0 * * * python3 <your path>/main.py
```

## 抽勇者福利社(廣告)
### Service
```ini
[Unit]
Description=巴哈自動抽獎

[Service]
User = <ssh使用者帳號>
WorkingDirectory = <路徑>
ExecStart = /usr/bin/python3 <lottery.py的路徑>
```

### Timer
```ini
[Unit]
Description=巴哈自動抽獎計時器

[Timer]
Unit=lottery.service
OnCalendar = *-*-* 00:10:00
OnCalendar = *-*-* 12:10:00

[Install]
WantedBy= multi-user.target
```

## 已加入的功能
自動簽到 2019-11-14

自動回答動畫瘋的問題 2020-11-24 新增

自動公會簽到 2020-12-06 新增

自動抽勇者福利社的獎品(廣告) 2021-01-22 新增

## config檔設定
將config_default.json重新命名為config.json
使用記事本等工具打開，並填入相關的資料

## 待加入的功能
自動回答勇者福利社的問題
