import os
import openai

from telegram import Update
from telegram.ext import ApplicationBuilder
from telegram.ext import filters
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes
from telegram.ext import MessageHandler

from constants import TELEGRAM_BOT_TOKEN
from constants import OPENAI_API_KEY
from constants import EMBEDDINGS_FILE
from search import ask
from search import get_embeddings
from utils import get_telegram_bot_username

# Load the embeddings into a dataframe object
df = get_embeddings(EMBEDDINGS_FILE)


def get_response(query):
    '''
    Search for question & answer in the provided document.
    If no matching question found, fetch from OpenAI.
    '''
    if not query or query == '' or len(query) < 2:
        print("Enter a valid question\n")
        return "Please ask me a valid question so that I can get you the answers you need!"
        
    response = ask(query=query, df=df, print_message=True)
    
    if not response:
        response = "Unfortunately I couldn't find the answer to your question. Please try rewording your question!"
        print("\nAnswer: ", response)
    
    print("----------------------------")

    return response


def is_bot_called(bot_username: str, message: str):
    return bot_username in message.lower() or '@bot' in message.lower()


async def handle_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'm a bot to help answer your questions, please ask me!")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    chat_type = update.message.chat.type
    message_text = str(update.message.text)

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) says: "{message_text}" in: {chat_type} chat')

    response = None
    bot_username = '@' + await get_telegram_bot_username(TELEGRAM_BOT_TOKEN)

    query = message_text.replace(bot_username, '')
    query = query.replace('@bot', '').strip()

    # Respond to group messages only if users mention the bot username
    if (chat_type == 'group' or chat_type == 'supergroup') and is_bot_called(bot_username, message_text):
        response = get_response(query)
    elif chat_type == 'private':
        response = get_response(query)

    if response:
        await update.message.reply_text(response)
        
    # TODO: else case: inform the user when there is no response instead of not replying at all 


# Run the program
def main():
    print('Starting up bot...')

    # Set the OpenAI API key
    openai.api_key = OPENAI_API_KEY

    # Uncomment when testing from command line, and comment out everything below
    # while True:
    #     text = input('> ')
    #     get_response(text)
    
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

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