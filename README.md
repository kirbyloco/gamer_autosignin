# 巴哈姆特自動簽到

登入程式碼參考
[XinBow99/BAHA_POSTER_Python](https://github.com/XinBow99/BAHA_POSTER_Python "XinBow99/BAHA_POSTER_Python")

## Linux排程
建議不要再00:00的時候執行，避免網路延遲導致無法簽到

自動回答問題是透過blackXblue小屋的答案回答，

所以排成建議設在00:10之後
```
10 0 * * * python3 <your path>/gamerautosign.py > /dev/null 2>&1
```

## 已加入的功能
自動簽到 2019-11-14

自動回答動畫瘋的問題 2020-11-24更新

## 待加入的功能
巴哈勇者福利社抽獎
