import pandas
import openai

from telegram import Update
from telegram.ext import ApplicationBuilder
from telegram.ext import filters
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler

from search import ask
from search import get_embeddings

# Telegram bot
TELEGROM_BOT_TOKEN = '6054419619:AAH3mx2PpvdZX1wnsPL09IF2jJIdRuFpF78'

# OpenAI API
openai.api_key = "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"

# FAQ file to load data from - TODO: read from local database
FAQ_FILE = 'data/binstarter_faq.xlsx'

# Load the embeddings
EMBEDDINGS_FILE = "data/embeddings.csv"
df = get_embeddings(EMBEDDINGS_FILE)


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

def translate(text):
    '''
    Send request to OpenAI to translate the given text to English.
    '''
    translate_prompt = '''Correct the grammatical mistakes in this sentence and translate to English if it's in another language:
    \n{}'''.format(text)
    
    response = get_openai_response(translate_prompt)

    return response

def translate_v2(text):
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

def get_response(query):
    '''
    Search for question & answer in the provided document.
    If no matching question found, fetch from OpenAI.
    '''
    if not query or query == '' or len(query) < 2:
        print("Enter a valid question\n")
        return "Please ask me a valid question so that I can get you the answers you need!"
    
    # translated_query = translate(query)
    
    response = ask(query=query, df=df, print_message=True)
    
    if not response:
        response = "Unfortunately I couldn't find the answer to your question. Please try rewording your question!"
        print("\nAnswer: ", response)
    
    print("----------------------------")

    return response


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm a bot to help answer your questions, please ask me!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    chat_type = update.message.chat.type
    message_text = str(update.message.text)
    response = ''

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) says: "{message_text}" in: {chat_type} chat')

    # Respond to group messages only if users mention the bot directly
    if chat_type == 'group' or chat_type == 'supergroup':
        # TODO: get the bot name programmaticaly since it will be different for each bot
        if '@freebot1_bot_bot' in message_text:
            new_text = message_text.replace('@freebot1_bot_bot', '').strip()
            response = get_response(new_text)
        if '@bot' in message_text:
            new_text = message_text.replace('@bot', '').strip()
            response = get_response(new_text)
    else:
        response = get_response(message_text)

    if response:
        await update.message.reply_text(response)
        
    # TODO: else case: inform the user when there is no response instead of not replying at all 


# Run the program
def main():
    print('Starting up bot...')

    # Uncomment when testing from command line, and comment out everything below
    # while True:
    #     text = input('> ')
    #     get_response(text)
    
    application = ApplicationBuilder().token(TELEGROM_BOT_TOKEN).build()

    # Add support for '/start' command
    start_handler = CommandHandler('start', handle_start)
    application.add_handler(start_handler)

    # Add message handler for all regular messages
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
    application.add_handler(message_handler)

    # Run the bot
    application.run_polling()


if __name__ == '__main__':
    main()