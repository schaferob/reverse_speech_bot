import os
from telegram.ext import Filters, CommandHandler, MessageHandler, Updater
import telegram as tg
import logging


log_level_env = os.environ.get("LOG_LEVEL")
LOG_LEVEL = None
if log_level_env == "debug":
    LOG_LEVEL=logging.DEBUG
elif log_level_env == "info":
    LOG_LEVEL=logging.INFO
else:
    LOG_LEVEL=logging.DEBUG
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from telegram.ext import Updater
import sys
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if BOT_TOKEN is '':
    sys.exit(0)

updater = Updater(token='TOKEN')
dispatcher = updater.dispatcher

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
print('test')
updater.start_polling()

