from flask import Blueprint
from flask import render_template

oral_assessment_bp = Blueprint('oral_assessment', __name__)

@oral_assessment_bp.route('/assess', methods=['GET'])
def assess():
    return render_template("assess.html")