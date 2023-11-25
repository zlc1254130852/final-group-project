import json, time
from setting import socketio

def generate_dify_speaking(response):
    tmp = ""
    for trunk in response:
        tmp += trunk.decode('utf-8').split("\n\n")[0]
        print(trunk.decode('utf-8'))
        print("---------------------")
        if len(trunk.decode('utf-8').split("\n\n")) >= 2:
            tmp2 = tmp[:].strip()
            tmp = trunk.decode('utf-8').split("\n\n")[-1]
            time.sleep(0.1)
            if len(tmp2) >= 6 and tmp2[0:6] == "data: " and 'answer' in json.loads(tmp2[6:]):
                socketio.emit('reply5', json.loads(tmp2[6:])['answer'])
        elif len(trunk.decode('utf-8')) >= 2 and trunk.decode('utf-8')[-2:] == "}\n":
            tmp3 = tmp[:].strip()
            tmp = ""
            time.sleep(0.1)
            if len(tmp2) >= 6 and tmp2[0:6] == "data: " and 'answer' in json.loads(tmp2[6:]):
                socketio.emit('reply5', json.loads(tmp3[6:])['answer'])