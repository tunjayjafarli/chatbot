import pandas
import openai

from telegram import Bot

async def get_telegram_bot_username(bot_token):
    bot = Bot(token=bot_token)
    bot_info = await bot.get_me()
    return bot_info.username

def get_openai_prompt(context_data, question):
    header = 'Answer the question as truthfully as possible using the provided context.' # , and if the answer is not contained within the context, say "I dont know."
    context = '\n'.join(context_data)
    prompt = header + "\n\n" + context + "\n\n Q: " + question + "\n A:"

    return prompt


def get_openai_response(prompt):
    '''
    Send request to OpenAI Completion API and return the response.
    '''
    # TODO: OpenAI request parameters
    try:
        print('OPENAI PROMPT: ', prompt)

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{prompt}",
            max_tokens=2048,
            n=1,
            stop=None,
            temperature=0.5,
        )

        print('OPENAI RESPONSE: ', response.choices[0].text.strip())
        # print('TOKEN USAGE: ', response.usage) # "usage": { "prompt_tokens": 5, "completion_tokens": 5, "total_tokens": 10 }
        return response.choices[0].text.strip()
    except Exception as e:
        print('Exception occurred while fetching from OpenAI: ', e)



def send_translate_request(text):
    '''
    Send request to OpenAI to translate the given text to English.
    '''
    translate_prompt = '''Correct the grammatical mistakes in this sentence and translate to English if it's in another language:
    \n{}'''.format(text)
    
    response = get_openai_response(translate_prompt)

    return response


def send_translate_request_v2(text):
    '''
    Send request to OpenAI to detect the language of question and translate it to English.
    '''
    translate_prompt = '''
    First, correct the grammatical mistakes in this sentence and answer the following:\n
    1. Determine the language
    2. Translate to English
    \n{}'''.format(text)
    
    response = get_openai_response(translate_prompt)

    if response:
        results = str(response).strip().split("\n")
        language = results[0].split(':')[1].strip()
        translation = results[1].split(':')[1].strip()
        return language, translation 
    else:
        return None, None


def open_file(file_name):
    '''
    Utility function to read file based on file extension.
    '''
    if 'xlsx' in file_name:
        return pandas.read_excel(file_name)
    elif 'csv' in file_name:
        return pandas.read_csv(file_name, sep=',')
    elif 'tsv' in file_name:
        return pandas.read_csv(file_name, sep='\t')
    else:
        print('Unsupported file type.')