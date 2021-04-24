import requests, json


# Send notifications to WeChat Work
def send_to_wechat_work(text):
    url_token = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
    res = requests.get(url=url_token, params={
        'corpid': 'ww426e0d497ab21cd2',  # 这里填写企业的获取到的corpID
        'corpsecret': 'P5U3S_kvLya_FaLJLw9_fk--oB4VXQO8WTmfh_RPMWc',  # 这里填写所创建应用的Secret
    }).json()
    token = res.get('access_token')
    url_msg = ' https://qyapi.weixin.qq.com/cgi-bin/message/send?'
    body = {
        "touser": "testuser",
        "msgtype": "text",
        "agentid": 1000003,  # 要调用的应用编号
        "text": {
            "content": text
        }
    }
    res = requests.post(url=url_msg, params={
        'access_token': token  # 这里是我们上面获取到的token
    }, data=json.dumps(body, ensure_ascii=False).encode('utf-8'))
