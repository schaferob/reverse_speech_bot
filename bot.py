import os
from telegram.ext import Filters, CommandHandler, MessageHandler, Updater
import telegram as tg
import logging
#for calling ffmpeg and sox
from subprocess import call


import logging
log_level_env = os.environ.get("LOG_LEVEL")
LOG_LEVEL = None
if log_level_env == "debug":
    LOG_LEVEL=logging.DEBUG
elif log_level_env == "info":
    LOG_LEVEL=logging.INFO
else:
    LOG_LEVEL=logging.INFO

logging.basicConfig(level=LOG_LEVEL,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

from telegram.ext import Updater
import sys
BOT_TOKEN = os.environ.get("BOT_TOKEN")
logging.info(f"Bot Token: {BOT_TOKEN}")
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
    #we use voice_key to namespace
    first_name = update.message.from_user.first_name
    voice_key = None
    if first_name is not None:
        last_name = update.message.from_user.last_name
        if last_name is not None:
            voice_key = f"{first_name}_{last_name}"
        else:
            voice_key = f"{first_name}"
    else:
        voice_key = str(update.message.from_user.id)
    
    voice_dir = "audio_assets"
    os.makedirs(voice_dir, exist_ok=True)

    ogg_filename = f'{voice_dir}/voice-{voice_key}.ogg'
    wav_filename = f'{voice_dir}/voice-{voice_key}.wav'
    mp3_filename = f'{voice_dir}/voice-{voice_key}.mp3'
    wav_filename_reversed = f'{voice_dir}/voice_reversed.wav'
    newFile.download(ogg_filename)
    print(call(['ffmpeg','-y', '-i',ogg_filename,wav_filename]))
    print(call(['sox', wav_filename, wav_filename_reversed,'reverse']))
    print(call(['ffmpeg','-y', '-i',wav_filename_reversed,mp3_filename]))
    #bot.send_message(chat_id=update.message.chat_id, text="Thanks for the audio clip. Soon I'll respond.")
    bot.send_audio(chat_id=update.message.chat_id, audio=open(mp3_filename, 'rb'))

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

from telegram.ext import MessageHandler, Filters

echo_handler = MessageHandler(Filters.all, echo)
dispatcher.add_handler(echo_handler)

print('test')
updater.start_polling()
updater.idle()

