# push.py
import requests
import os

def push_serverchan(title, content):
    sendkey = os.environ.get("SERVERCHAN_KEY")
    if not sendkey:
        print("未设置 Server 酱 SendKey，跳过推送")
        return
    url = f"https://sctapi.ftqq.com/{sendkey}.send"
    data = {
        "title": title,
        "desp": content
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("方糖通知发送成功")
        else:
            print(f"方糖通知失败：{response.text}")
    except Exception as e:
        print(f"方糖推送异常: {e}")
