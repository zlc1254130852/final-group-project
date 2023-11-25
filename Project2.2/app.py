# -*- encoding:utf-8 -*-
# main.py
from setting import app
from blueprint import build_blueprint

build_blueprint(app)

print("Server ready")

if __name__ == '__main__':

    app.run(host='0.0.0.0', debug=True)

