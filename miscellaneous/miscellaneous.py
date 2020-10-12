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
