import requests
import json
import os

if __name__ == '__main__':
    # Server酱秘钥
    sckey = os.environ.get("SERVER_CHAN_SCKEY", "")

    # 推送内容
    title = ""
    success, fail, repeats = 0, 0, 0        
    sendContent = ""

    # glados账号cookie
    cookies = os.environ.get("COOKIES", []).split("&")
    if cookies[0] == "":
        print('未获取到COOKIE变量')
        cookies = []
        exit(0)

    url = "https://glados.rocks/api/user/checkin"
    url2 = "https://glados.rocks/api/user/status"

    referer = 'https://glados.rocks/console/checkin'
    origin = "https://glados.rocks"
    useragent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    payload = {
        'token': 'glados.one'
    }

    for cookie in cookies:
        checkin = requests.post(url, headers={'cookie': cookie, 'referer': referer, 'origin': origin,
                                'user-agent': useragent, 'content-type': 'application/json;charset=UTF-8'}, data=json.dumps(payload))
        state = requests.get(url2, headers={
                             'cookie': cookie, 'referer': referer, 'origin': origin, 'user-agent': useragent})

        if checkin.status_code == 200:
            result = checkin.json()
            status = result.get('message')
            result = state.json()
            leftdays = int(float(result['data']['leftDays']))
            email = result['data']['email']
            
            print(status)
            if "Checkin!" in status:
                success += 1
                message_status = "签到成功，会员天数 + 1"
            elif status == "Checkin Repeats! Please Try Tomorrow":
                message_status = "今日已签到"
            else:
                fail += 1
                message_status = "签到失败，请检查..."

            if leftdays is not None:
                message_days = f"{leftdays} 天"
            else:
                message_days = "无法获取剩余天数信息"
        else:
            email = ""
            message_status = "签到请求url失败, 请检查..."
            message_days = "获取信息失败"

        sendContent += f"{status}\n\
            {'-'*30}\n\
            账号: {email}\n\
            签到情况: {message_status}\n\
            status字段: {status}\n\
            剩余天数: {message_days}\n"
        
        if cookie == cookies[-1]:
            sendContent += '-' * 30

    print("sendContent:" + "\n", sendContent)
    
    # Server酱推送
    if SERVER_CHAN_SCKEY != "":
        title = f'成功{success},失败{fail},重复{repeats}'
        server_chan_url = "https://sctapi.ftqq.com/{SERVER_CHAN_SCKEY}.send?text={title}&desp={sendContent}"
        r = requests.get(server_chan_url)
        print(r.status_code)
