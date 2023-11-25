from flask import Blueprint
from flask import render_template
from flask import request
from AI_chat import openai_client

text_summary_bp = Blueprint('text_summary', __name__)

@text_summary_bp.route('/text_summary', methods=['GET'])
def text_summary():
    return render_template("text_summary.html")

@text_summary_bp.route('/summarize', methods=['POST'])
def summarize():
    result = text_summarizing(request.values["text"])
    print(result)
    return {'result': result}

def meeting_minutes(transcription):
    abstract_summary = abstract_summary_extraction(transcription)
    key_points = key_points_extraction(transcription)
    return {
        'abstract_summary': abstract_summary,
        'key_points': key_points
    }

def abstract_summary_extraction(transcription):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a highly skilled AI trained in language comprehension and summarization. I would like you to read the following text and summarize it into a concise abstract paragraph. Aim to retain the most important points, providing a coherent and readable summary that could help a person understand the main points of the discussion without needing to read the entire text. Please avoid unnecessary details or tangential points."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response.choices[0].message.content


def key_points_extraction(transcription):
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "You are a proficient AI with a specialty in distilling information into key points. Based on the following text, identify and list the main points that were discussed or brought up. These should be the most important ideas, findings, or topics that are crucial to the essence of the discussion. Your goal is to provide a list that someone could read to quickly understand what was talked about."
            },
            {
                "role": "user",
                "content": transcription
            }
        ]
    )
    return response.choices[0].message.content

def text_summarizing(transcription):
    minutes = meeting_minutes(transcription)
    print(minutes)
    return minutes