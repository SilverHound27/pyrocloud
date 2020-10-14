import time
import asyncio
from miscellaneous.locks import locks

def status(client, message):
    message.reply_text("I'm alive :)")

def start(client, message):
    message.reply_text('HELLO WORLD')

def train(client, message):
    if not locks['train']:
        return
    message.reply_sticker("CAADAgADKAMAArVx2gaQekqHXpVKbhYE")

async def m_info(client, message):
    a = await message.reply_text(message.reply_to_message)
    await message.delete()
    await asyncio.sleep(60)
    await a.delete()

async def help_fn(client, message):
    help_str = '''Youtube: Send me a youtube link or reply '/yt' to a youtube link\n
                  Upload: reply /upload to a link\n
                  Get download links: Send me a link'''
    a = await message.reply_text(help_str)
    await asyncio.sleep(60)
    await message.delete()
    await a.delete()