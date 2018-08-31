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
    LOG_LEVEL=logging.INFO
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from telegram.ext import Updater
import sys
BOT_TOKEN = os.environ.get("BOT_TOKEN")
print(BOT_TOKEN)
if BOT_TOKEN is '':
    sys.exit(0)

updater = Updater(token=BOT_TOKEN)
dispatcher = updater.dispatcher

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
def echo(bot, update):
    if update.message.voice is None:
        bot.send_message(chat_id=update.message.chat_id, text="Send me an audio clip!")
        return
    file_id = update.message.voice.file_id
    print(f"File id: {file_id}")
    newFile = bot.get_file(file_id)
    print(f"New file: {newFile}")
    newFile.download('voice.ogg')
    bot.send_message(chat_id=update.message.chat_id, text="Thanks for the audio clip. Soon I'll respond with ")
    #bot.send_audio(chat_id=update.message.chat_id, audio=open('voice.ogg', 'rb'))

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

from telegram.ext import MessageHandler, Filters

echo_handler = MessageHandler(Filters.all, echo)
dispatcher.add_handler(echo_handler)

print('test')
updater.start_polling()
updater.idle()

