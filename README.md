# 巴哈姆特自動簽到

登入程式碼參考
[XinBow99/BAHA_POSTER_Python](https://github.com/XinBow99/BAHA_POSTER_Python "XinBow99/BAHA_POSTER_Python")

## Linux排程
建議不要再00:00的時候執行，避免網路延遲導致無法簽到
```
5 0 * * * python3 /home/kltw/bot/gamerautosign.py > /dev/null 2>&1
```

## 待加入的功能
巴哈動畫瘋回答題目
