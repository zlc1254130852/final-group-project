import json, time
from hashlib import md5
import random
import requests
from setting import socketio
import websocket

app_id = ""
api_key = ""
# Set your own appid/appkey.
appid = ''
appkey = ''

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'en'
to_lang =  'zh'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

class Client():
    def __init__(self):
        self.to_lang="zh"
        self.end_tag = "{\"end\": true}"

    def send(self, data):
        self.ws.send(data)
        time.sleep(0.04)

    def stop_send(self):
        self.ws.send(bytes(self.end_tag.encode('utf-8')))
        print("send end tag success")

    def recv(self):
        try:
            while self.ws.connected:
                result = str(self.ws.recv())
                if len(result) == 0:
                    print("receive result end")
                    self.ws.close()
                    print("connection closed")
                    break
                result_dict = json.loads(result)

                if result_dict["action"] == "started":
                    print("handshake success, result: " + result)
                    socketio.emit('reply', {"result": " \n----------------\nconnected\n----------------\n", "end": 1})

                if result_dict["action"] == "result":
                    result_1 = result_dict
                    result_2 = json.loads(result_1["data"])
                    result_3 = ""
                    end_tag = ""
                    end=len(result_2["cn"]["st"]["rt"][0]["ws"])
                    result_4=result_2["cn"]["st"]["rt"][0]["ws"]
                    for i in range(0,end):
                        result_3 += result_4[i]["cw"][0]["w"]
                    end_tag = result_2["cn"]["st"]["ed"]

                    if end_tag == "0":
                        socketio.emit('reply', {"result": result_3, "end": 0})

                    else:
                        socketio.emit('reply',{"result":result_3,"end":1})

                        if result_3 and result_3[0] in [',','.','?','!']:
                            if len(result_3)>1:
                                result_3=result_3[1:len(result_3)]
                            else:
                                result_3=" "
                        salt = random.randint(32768, 65536)
                        # Build request
                        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                        sign = make_md5(appid + result_3 + str(salt) + appkey)
                        payload = {'appid': appid, 'q': result_3, 'from': from_lang, 'to': self.to_lang, 'salt': salt, 'sign': sign}
                        r = requests.post(url, params=payload, headers=headers)
                        result = r.json()
                        if "trans_result" in result:
                            socketio.emit('reply', {"result": " "+result["trans_result"][0]["dst"],"end":1})

                if result_dict["action"] == "error":
                    print("rtasr error: " + result)
                    self.ws.close()
                    return

        except websocket.WebSocketConnectionClosedException:
            print("receive result end")

    def close(self):
        self.ws.close()
        print("connection closed")