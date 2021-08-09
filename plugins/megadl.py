# The code you are about to see below is a work of an absolute(100%) noob. 
# Ok now go ahead you will see what I mean!

# Solely coded by xmysteriousx

import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import asyncio
import json
import math
import subprocess
import os
import shutil
import time
from datetime import datetime
from asyncio import get_running_loop

from helpers.download_uplaod_helper import send_splitted_file, send_file
from helpers.files_spliiting import split_files

from functools import partial

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

from translation import Translation

import pyrogram
from pyrogram import Client, filters

from pyrogram.errors import UserNotParticipant, UserBannedInChannel
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

logging.getLogger("pyrogram").setLevel(logging.WARNING)

from database.blacklist import check_blacklist
from database.userchats import add_chat

from mega import Mega

mega = Mega()

# It is really not imprtant for you to enter your mega email or password in config variables!
if Config.Mega_email is not None and Config.Mega_password is not None:
    email = Config.Mega_email
    password = Config.Mega_password
    m = mega.login(email, password)
else:
    m = mega.login() # Here we make an anonymous, temporary account!
    

def download_with_progress(megalink, tmp_directory_for_each_user, usermsg, time_for_mega):
    try:
        m.download_url(megalink, tmp_directory_for_each_user, progress_msg_for_mega=usermsg, process_start_time=time_for_mega)
    except Exception as e:
        logger.info(e)
