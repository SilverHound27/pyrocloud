import time
import threading

def status(client, message):
    message.reply_text("I'm alive :)")

def start(client, message):
    message.reply_text('HELLO WORLD')

def train(client, message):
    message.reply_sticker("CAADAgADKAMAArVx2gaQekqHXpVKbhYE")

def msg_info(client, message):
    a = message.reply_text(message.reply_to_message)
    time.sleep(60)
    a.delete()

def m_info(c, m):
    t = threading.Thread(target=msg_info, args=(c,m))
    t.start()