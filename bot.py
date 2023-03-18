from telegram.ext import *
import openai
import pandas as pd
from thefuzz import fuzz
from thefuzz import process

# Telegram bot
bot_token = '6054419619:AAH3mx2PpvdZX1wnsPL09IF2jJIdRuFpF78'

# OpenAI API
openai.api_key = "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"

# Database - TODO: read from local database
file_path = 'faq.tsv'
df = pd.read_csv(file_path, sep="\t")


def start_command(update, context):
    update.message.reply_text('Hello there! I\'m a bot. What\'s up?')


def handle_response(query):
    '''
    Search for question & answer in the provided document.
    If no matchng question found, fetch from OpenAI.
    '''
    if not query or query == '' or len(query) < 2:
        print("Enter a valid question\n")
        return "Enter a valid question."

    question_list = df['Question'].tolist()

    result = process.extractOne(
        query, 
        question_list, 
        scorer=fuzz.token_set_ratio, 
        score_cutoff=75
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
        

def handle_message(update, context):
    # Get basic info of the incoming message
    message_type = update.message.chat.type
    text = str(update.message.text).lower()
    response = ''

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) says: "{text}" in: {message_type}')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # TODO: get the bot name programmaticaly since it will be different for each customer
        if '@freebot1_bot_bot' in text:
            new_text = text.replace('@freebot1_bot_bot', '').strip()
            response = handle_response(new_text)
    else:
        response = handle_response(text)

    # Reply normal if the message is in private
    update.message.reply_text(response)


# Log errors
def error(update, context):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    print('Starting up bot...')

    updater = Updater(bot_token)
    dp = updater.dispatcher

    # Commands
    dp.add_handler(CommandHandler('start', start_command))

    # Messages
    dp.add_handler(MessageHandler(Filters.text, handle_message))

    # Log all errors
    dp.add_error_handler(error)

    # Run the bot
    updater.start_polling(1.0)
    updater.idle()