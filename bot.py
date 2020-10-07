from pyrogram import Client, Filters
from creds import Config
from random import randint
from progress import progress_for_pyrogram
import time
import os
app = Client(
        "new",
        bot_token=Config.TG_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
    )

def progress(current, total):
    print(f"{current * 100 / total:.1f}%")

@app.on_message(Filters.text)
def echo(client, message):
    message.reply_text(message.text)

@app.on_message(Filters.document)
def echo(client, message):
    a = message.reply_text('doc found')
    c_time = time.time()
    file_path = client.download_media(message= message,
                    progress=progress_for_pyrogram,
                    progress_args=("Starting dl", a, c_time )
                    )
    print(file_path)


app.run()  # Automatically start() and idle()