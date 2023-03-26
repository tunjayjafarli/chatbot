import pandas
import openai

from telegram import Update
from telegram.ext import ApplicationBuilder
from telegram.ext import filters
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler

from thefuzz import fuzz
from thefuzz import process

# Telegram bot
TELEGROM_BOT_TOKEN = '6054419619:AAH3mx2PpvdZX1wnsPL09IF2jJIdRuFpF78'

# OpenAI API
openai.api_key = "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"

# FAQ file to load data from - TODO: read from local database
FAQ_FILE = 'binstarter_faq.xlsx'


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


def get_response(query):
    '''
    Search for question & answer in the provided document.
    If no matching question found, fetch from OpenAI.
    '''
    if not query or query == '' or len(query) < 2:
        print("Enter a valid question\n")
        return "Enter a valid question."

    df = open_file(FAQ_FILE)
    question_list = df['Question'].tolist()

    result = process.extractOne(
        query, 
        question_list, 
        scorer=fuzz.partial_token_sort_ratio, 
        score_cutoff=70
    )

    if result is not None and result[0] and len(result[0]) > 3:
        matchingQuestion, score = result
        answer = df.loc[df['Question'] == matchingQuestion].iloc[0]['Answer']

        print("Question found: ", matchingQuestion, "Score: ", score)
    else:
        print("No matching question found. Asking OpenAI...\n")

        # Fetch from OpenAI
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"{query}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )
        answer = response.choices[0].text
        
    print("Answer: ", answer)
    print("----------------------------")

    return answer


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm a bot to help answer your questions, please ask me!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    chat_type = update.message.chat.type
    message_text = str(update.message.text).lower()
    response = ''

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) says: "{message_text}" in: {chat_type} chat')

    # Respond to group messages only if users mention the bot directly
    if chat_type == 'group' or chat_type == 'supergroup':
        # TODO: get the bot name programmaticaly since it will be different for each customer
        if 'bot' in message_text or '@freebot1_bot_bot' in message_text:
            new_text = message_text.replace('@freebot1_bot_bot', '').strip()
            response = get_response(new_text)
    else:
        response = get_response(message_text)

    if response:
        await update.message.reply_text(response)


# Run the program
def main():
    print('Starting up bot...')

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