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
import redis
cache = redis.Redis(host='redis', port=6379)
DEFAULT_AUDIO_OUTPUT_FORMAT = "voice"
AVAILABLE_OUTPUT_FORMATS = ["ogg","wav","mp3",'voice']

from redis_helpers import *


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please talk to me!")
def echo(bot, update):
    if update.message.voice is None:
        bot.send_message(chat_id=update.message.chat_id, text="Send me an audio clip!")
        return
    #TODO: add support for reading from audio instead of just voice
    bot.send_chat_action(chat_id=update.message.chat_id, action=tg.ChatAction.UPLOAD_AUDIO)
    file_id = update.message.voice.file_id
    newFile = bot.get_file(file_id)
    
    #we use voice_key to namespace
    voice_key = f"{update.message.from_user.id}_{update.message.chat_id}"
    logging.info(f"voice_key: {voice_key}")
    voice_dir = "audio_assets"
    os.makedirs(voice_dir, exist_ok=True)

    base_filename = f'{voice_dir}/voice-{voice_key}'
    ogg_filename = f'{base_filename}.ogg'
    wav_filename = f'{base_filename}.wav'
    wav_filename_reversed = f'{base_filename}-reversed.wav'

    newFile.download(ogg_filename)  
    logging.debug(call(['ffmpeg','-y', '-i',ogg_filename,wav_filename]))
    logging.debug(call(['sox', wav_filename, wav_filename_reversed,'reverse']))
    desired_output_format = get_output_for_user(update.message.from_user.id,cache)
    if desired_output_format == 'voice':
        output_filename = f"{base_filename}.mp3" 
    else:
        output_filename = f"{base_filename}.{desired_output_format}" 
    logging.info(f"output_filname: {output_filename}")
    logging.debug(call(['ffmpeg','-y', '-i',wav_filename_reversed,output_filename]))
    #bot.send_message(chat_id=update.message.chat_id, text="Thanks for the audio clip. Soon I'll respond.")
    if desired_output_format == 'voice':
        bot.send_voice(chat_id=update.message.chat_id, voice=open(output_filename, 'rb'))
    else:
        bot.send_audio(chat_id=update.message.chat_id, audio=open(output_filename, 'rb'))
    


def set_output_format(bot, update, args):
    args_length = len(args)
    command_help_message = "Use command like: /setoutputformat mp3"
    if args_length == 0 or args_length >1 :
        bot.send_message(chat_id=update.message.chat_id, text=command_help_message)
        return
    user_id = update.message.from_user.id
    output_format = args[0]
    if output_format not in AVAILABLE_OUTPUT_FORMATS:
        message = f"Choose one of the following formats: {' '.join(AVAILABLE_OUTPUT_FORMATS)}."
        bot.send_message(chat_id=update.message.chat_id, text=message)
        return

    logging.info(f"Set output format: {output_format}")
    set_output_for_user(user_id, output_format, cache)
    message = f"Desired output format set to: {output_format}"
    bot.send_message(chat_id=update.message.chat_id, text=message)

def get_output_format(bot,update):
    user_id = update.message.from_user.id
    output_format = get_output_for_user(user_id, cache)
    message = f"Output Format: {output_format}"
    bot.send_message(chat_id=update.message.chat_id, text=message)

def main():
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    logging.info(f"Bot Token: {BOT_TOKEN}")
    if BOT_TOKEN is '':
        sys.exit(0)

    updater = Updater(token=BOT_TOKEN)
    dispatcher = updater.dispatcher

    echo_handler = MessageHandler(Filters.voice, echo)
    dispatcher.add_handler(echo_handler)

    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    set_output_format_handler = CommandHandler('setoutputformat', set_output_format, pass_args=True)
    dispatcher.add_handler(set_output_format_handler)
    get_output_format_handler = CommandHandler('getoutputformat', get_output_format)
    dispatcher.add_handler(get_output_format_handler)

    logging.info("Start polling")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()