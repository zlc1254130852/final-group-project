import openai
from utils import text_chunking,timer
from log_api_file import log_api
import pickle
import time
from retry import retry

global deployment_name

global first_prompt
first_prompt =  f'''
           You are an OpenAI language model proficient in summarization.\n
           we are summarizing a text and highlightig important notes in it.\n
           we have divided the text into multiple chunks. we are trying to do recursive summarization.\n
            '''
# Define a temporary placeholder for previous_summary
previous_summary_placeholder = "<previous_summary_placeholder>"

global prompt
prompt= f""" 
We are summarizing a text and highlight important notes in text as bullet point.\n
 
INSTRUCTION:
Could you please give a combined concise summary of the next chunk and previous summary.\n

The summary of previous chunk is:\n
"<{previous_summary_placeholder}>"\n

IMPORTANT RULE:\n
1.If the new chunk has unrelated data ignore it and please not to give the summary of previous chunks.\n

The desired response format is:\n
Summary:
"""


@retry(delay=0, backoff=1, max_delay=10,tries=5)
def azure_openai_request(param1,param2):
    response = openai.ChatCompletion.create(
        engine="chatgpt-demo",
        temperature=0,
        request_timeout=10,
        messages=[
            {"role": "system", "content": param1},
            {"role": "user", "content": f"In the following you can find the chunk of webpage: {param2}"},
        ]
    )
    return response


@timer
def azure_response(text):

    print('summarize text')
    chunks = text_chunking(text)

    prompt_identifier = "Summarize"

    for i in range(0, len(chunks)):
        try:
            start = time.time()
            if i == 0:
                response = azure_openai_request(first_prompt,chunks[i])
            else:
                previous_summary = response['choices'][0]['message']['content']
                global prompt
                prompt = prompt.replace(previous_summary_placeholder, previous_summary)
                response = azure_openai_request(first_prompt,chunks[i])
            r_time = time.time() - start
            log_api(username, project_name, prompt_identifier, response, str(round(r_time, 2)), error='')
            return_value =  response['choices'][0]['message']['content']
        except Exception as e:
            exception_string = str(e).replace("\n", "\\n")
            log_api(username, project_name, prompt_identifier, '', '0', error=exception_string)
            if "TimeOut" in exception_string:
                pass
            else:
                return_value = "Azure API failed"
                continue
    print('end text\n')
    return return_value


def text_chunking_v2(text):
    # use NLTK to tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    max_tokens_per_segment = 1900

    # initialize variables for keeping track of segments
    current_segment = ''
    segments = []

    # loop through each sentence in the text
    for sentence in sentences:
        # check if all sentences of a comment are within a segment if not add next sentence.
        if (str(current_segment)).count('*#') % 2 != 0:
            current_segment += sentence + ' '
            print(current_segment)
        else:
            # if adding the current sentence to the current segment would exceed the max tokens per segment,
            # add the current segment to the list of segments and start a new segment
            if len(current_segment.split()) + len(sentence.split()) > max_tokens_per_segment:
                segments.append(current_segment)
                current_segment = ''

            # add the current sentence to the current segment
            current_segment += sentence + ' '

    # add the final segment to the list of segments
    segments.append(current_segment)

    return segments
    
def text_chunking(text):
    # use NLTK to tokenize the text into sentences
    sentences = nltk.sent_tokenize(text)
    max_tokens_per_segment = 1900

    # initialize variables for keeping track of segments
    current_segment = ''
    segments = []

    # loop through each sentence in the text
    for sentence in sentences:
        # if adding the current sentence to the current segment would exceed the max tokens per segment,
        # add the current segment to the list of segments and start a new segment
        if len(current_segment.split()) + len(sentence.split()) > max_tokens_per_segment:
            segments.append(current_segment)
            current_segment = ''
        # add the current sentence to the current segment
        current_segment += sentence + ' '

    # add the final segment to the list of segments
    segments.append(current_segment)

    return segments