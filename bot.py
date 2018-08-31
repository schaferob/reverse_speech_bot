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


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
def echo(bot, update):
    if update.message.voice is None:
        bot.send_message(chat_id=update.message.chat_id, text="Send me an audio clip!")
        return
    file_id = update.message.voice.file_id
    logging.debug(f"File id: {file_id}")
    newFile = bot.get_file(file_id)
    logging.debug(f"New file: {newFile}")
    #we use voice_key to namespace
    voice_key = f"{str(update.message.from_user.id)}_{str(update.message.chat_id)}"
    logging.info(f"voice_key: {voice_key}")
    voice_dir = "audio_assets"
    os.makedirs(voice_dir, exist_ok=True)

    ogg_filename = f'{voice_dir}/voice-{voice_key}.ogg'
    wav_filename = f'{voice_dir}/voice-{voice_key}.wav'
    wav_filename_reversed = f'{voice_dir}/voice_reversed.wav'
    newFile.download(ogg_filename)  
    logging.debug(call(['ffmpeg','-y', '-i',ogg_filename,wav_filename]))
    logging.debug(call(['sox', wav_filename, wav_filename_reversed,'reverse']))
    output_filename = ogg_filename
    logging.debug(call(['ffmpeg','-y', '-i',wav_filename_reversed,output_filename]))
    #bot.send_message(chat_id=update.message.chat_id, text="Thanks for the audio clip. Soon I'll respond.")
    bot.send_audio(chat_id=update.message.chat_id, audio=open(output_filename, 'rb'))





def main():
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    logging.info(f"Bot Token: {BOT_TOKEN}")
    if BOT_TOKEN is '':
        sys.exit(0)

    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    echo_handler = MessageHandler(Filters.all, echo)
    dispatcher.add_handler(echo_handler)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    logging.info("Start polling")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()