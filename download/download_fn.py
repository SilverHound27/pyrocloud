import os
import subprocess
from urllib.parse import unquote
import time
from pySmartDL import SmartDL
from random import choice
import asyncio
from pyrogram.errors import FloodWait

glitch = ['( ͡° ͜ʖ ͡°)', '¯\_(ツ)_/¯', '̿̿ ̿̿ ̿̿ ̿\̿\'\̵͇̿̿\з= ( ▀ ͜͞ʖ▀) =ε/̵͇̿̿/’̿’̿ ̿ ̿̿ ̿̿ ̿̿', '¯\_(ツ)_/¯','ʕ•ᴥ•ʔ', '(ง ͠° ͟ل͜ ͡°)ง', '(;´༎ຶД༎ຶ`)']


async def smart_dl(url, update):

    temp_name = unquote(url).split("/")[-1]
    dest = os.path.join(os.getcwd(), str(update.from_user.id), temp_name)

    obj = SmartDL(url, dest, progress_bar= False)
    obj.start(blocking = False)

    while not obj.isFinished():
        try:
            stats = "FileName: {} \nProgress: {:.2f}% \nSpeed: {} \nDownloaded: {}/{} \nStatus:{} \nEstimated time: {} \n    {}  ".format(
                temp_name, (obj.get_progress()*100), obj.get_speed(human=True), obj.get_dl_size(human=True), obj.get_final_filesize(human=True),
                obj.get_status(), obj.get_eta(human=True), obj.get_progress_bar())
            
            await update.message.edit(stats)
            await asyncio.sleep(5)
        except FloodWait as s:
            await asyncio.sleep(s.x)
        except:
            await asyncio.sleep(10)

    if obj.isSuccessful():
        filename = obj.get_dest().split('/')[-1]
        download_time = obj.get_dl_time(human=True)
    else:
        filename = False
        download_time = "NA"
        dest = False
    return dest


def wget_dl(url):
        try:
            print("Downloading Started")

            filename = unquote(url.split('/')[-1])
            output = subprocess.check_output("wget '--output-document' '{}' '{}' ".format(filename , url), stderr=subprocess.STDOUT, shell=True)
            
            print("Downloading Complete",filename)
            return filename
        except Exception as e:
            print("DOWNLAOD ERROR :",e)
           
            return "error",filename