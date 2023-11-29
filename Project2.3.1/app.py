# -*- encoding:utf-8 -*-
# main.py
from setting import app, db
from blueprint import build_blueprint

print("Server ready")

build_blueprint(app)

# Uncomment the code below to initialize the tables and records in the database
# db.create_all()   # create all tables

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)

# @app.route('/reading/<id>',methods=['GET'])
# def reading(id):
#     return render_template("reading/reading"+id+".html")
#
# @app.route('/listening/<id>',methods=['GET'])
# def listening(id):
#     return render_template("listening/listening"+id+".html")

