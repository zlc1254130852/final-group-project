from flask import Blueprint
from flask import render_template

real_time_translation_bp = Blueprint('real_time_translation', __name__)


@real_time_translation_bp.route('/voice', methods=['GET'])
def voice():
    return render_template("voice.html")