# -*- encoding:utf-8 -*-
# main.py

from flask import render_template, request
from setting import app, db
from blueprint import build_blueprint
from tables import Answers
from login_check import check_login
from tables import Record

print("Server ready")

build_blueprint(app)

# Uncomment the code below to initialize the tables and records in the database
# db.drop_all()
# db.create_all()   # create all tables
# listening_answers_list=[["Jamieson","afternoon","communication","week","10","suit","passport","personality","feedback","time"],['A','B','A','C','river','1422','top','pass','steam','capital'],['G','F','A','E','B','C','C','A','B','D'],['shelter','oil','roads','insects','grass','water','soil','dry','simple','nests']]
# reading_answers_list=[['oval','husk','seed','mace','FALSE','NOT GIVEN','TRUE','Arabs','plague','lime','Run','Mauritius','tsunami'],['C','B','E','G','D','human error','car-sharing','ownership','mileage','C','D','A','E'],['A','C','C','D','A','B','E','A','D','E','B','expeditions','isolated','land surface']]
#
# for i in range(0,4): # initialize the info for the test answers
#     model_answer = Answers()
#     model_answer.practice_name = "listening"+str(i+1)
#     model_answer.content = str(listening_answers_list[i])
#     db.session.add(model_answer)
#     db.session.commit()
#
# for i in range(0,3): # initialize the info for the test answers
#     model_answer = Answers()
#     model_answer.practice_name = "reading"+str(i+1)
#     model_answer.content = str(reading_answers_list[i])
#     db.session.add(model_answer)
#     db.session.commit()

@app.route('/reading/<id>',methods=['GET'])
def reading(id):
    user_info = check_login()  # check which user is logged in.

    if user_info:  # if there is a logged-in user
        return render_template("reading/reading"+id+".html", current_user=user_info.login_name)
    else:
        return render_template("reading/reading"+id+".html")

@app.route('/listening/<id>',methods=['GET'])
def listening(id):
    user_info = check_login()  # check which user is logged in.

    if user_info:  # if there is a logged-in user
        return render_template("listening/listening"+id+".html", current_user=user_info.login_name)
    else:
        return render_template("listening/listening"+id+".html")

@app.route('/submit/<practice_name>',methods=['GET'])
def submit(practice_name):
    answer = Answers.query.filter_by(practice_name=practice_name).first()
    return eval(answer.content)

@app.route('/save',methods=['POST'])
def save():
    req = request.values
    current_user = req['current_user']
    practice_name = req['practice_name']
    answers_to_save = req['answers_to_save']

    print(eval(answers_to_save))

    record_info = Record.query.filter_by(user_name=current_user, practice_name=practice_name).first()
    if record_info:
        print(record_info)
        db.session.delete(record_info)
        db.session.commit()

    model_record = Record()
    model_record.user_name = current_user
    model_record.practice_name = practice_name
    model_record.content = answers_to_save
    db.session.add(model_record)
    db.session.commit()

    return {"code":200}

@app.route('/load',methods=['POST'])
def load():
    req = request.values
    current_user = req['current_user']
    practice_name = req['practice_name']

    record_info = Record.query.filter_by(user_name=current_user, practice_name=practice_name).first()
    print(record_info)
    if record_info:
        return {"record_info": eval(record_info.content), "code":200}
    else:
        return {"record_info": "", "code":-1}

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)
