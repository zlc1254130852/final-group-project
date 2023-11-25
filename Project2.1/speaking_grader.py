from flask import Blueprint
from flask import render_template

speaking_grader_bp = Blueprint('speaking_grader', __name__)

@speaking_grader_bp.route('/upload',methods=['GET'])
def upload():
    return render_template("upload.html")