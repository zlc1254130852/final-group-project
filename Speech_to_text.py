from openai import OpenAI

client = OpenAI(api_key='')

def transcribe(file_name: str= 'Recording.m4a'):
  """
  uses to do speech to text based on voice of user which stored in directory.
  :param file_name: name of recorded
  :return: the text associated with audio file.
  """

  audio_file= open(f".//audio/{file_name}", "rb")
  transcript = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
  )

  text = transcript['text']

  return text

