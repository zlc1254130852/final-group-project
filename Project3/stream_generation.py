# -*- encoding:utf-8 -*-
import json, time
from setting import socketio
from tables import Message
from setting import db
import datetime

def generate_AI_chat(current_user,app_type,message_id,ctrler,opt,response):
    tmp_message=""
    for trunk in response:
        if ctrler[opt]==0:
            if trunk.choices[0].delta.content:
                tmp_message+=trunk.choices[0].delta.content
            time.sleep(0.1)
            yield json.dumps({'delta':trunk.choices[0].delta.content,'finish_reason':trunk.choices[0].finish_reason}) + "\n"
        else:
            model_message = Message()
            model_message.user_name = current_user
            model_message.app_type = app_type
            model_message.message_id = str(message_id + 1)
            model_message.content = str({"role": "assistant", "content": tmp_message})
            # model_message.created_time = datetime.datetime.now()
            db.session.add(model_message)
            db.session.commit()
            return
    model_message = Message()
    model_message.user_name = current_user
    model_message.app_type = app_type
    model_message.message_id = str(message_id+1)
    model_message.content = str({"role": "assistant", "content": tmp_message})
    # model_message.created_time = datetime.datetime.now()
    db.session.add(model_message)
    db.session.commit()

def generate_bwav(bwav):
    for i in range(len(bwav)//1024+1):
        if (i+1)*1024>len(bwav):
            tmp=[]
            for j in range(1024-len(bwav)%1024):
                tmp.append(0)

            yield bwav[i*1024:len(bwav)]+bytes(tmp)
        else:
            yield bwav[i*1024:(i+1)*1024]

def generate_dify_writing(response):
    tmp = ""
    for trunk in response:
        tmp += trunk.decode('utf-8').split("\n\n")[0]
        print(trunk.decode('utf-8'))
        print("---------------------")
        if len(trunk.decode('utf-8').split("\n\n")) >= 2:
            tmp2 = tmp[:].strip()
            tmp = trunk.decode('utf-8').split("\n\n")[-1]
            time.sleep(0.1)
            if len(tmp2) >= 6 and tmp2[0:6] == "data: ":
                yield tmp2
        elif len(trunk.decode('utf-8')) >= 2 and trunk.decode('utf-8')[-2:] == "}\n":
            tmp3 = tmp[:].strip()
            tmp = ""
            time.sleep(0.1)
            if len(tmp2) >= 6 and tmp2[0:6] == "data: ":
                yield tmp3

def generate_dify_speaking(response,user):
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
                socketio.emit('reply5', {"user":user,"result":json.loads(tmp2[6:])['answer']})
        elif len(trunk.decode('utf-8')) >= 2 and trunk.decode('utf-8')[-2:] == "}\n":
            tmp3 = tmp[:].strip()
            tmp = ""
            time.sleep(0.1)
            if len(tmp2) >= 6 and tmp2[0:6] == "data: " and 'answer' in json.loads(tmp2[6:]):
                socketio.emit('reply5', {"user":user,"result":json.loads(tmp3[6:])['answer']})
