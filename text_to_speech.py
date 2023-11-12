from pathlib import Path
from openai import OpenAI

client = OpenAI(api_key='')

def text_to_speech(text: str = 'Hello Please enter your text', name: str = 'audio'):
    """

    :param text: the user text to generate audio file
    :param name: name for audio file
    :return: it converts text to speech
    """
    speech_file_path = Path(__file__).parent / "Audio" / f"{name}.mp3"
    response = client.audio.speech.create(
      model="tts-1",
      voice="alloy",
      input=text
    )

    response.stream_to_file(speech_file_path)
    return 'Success'