from pyrogram import Client, filters
import pyrogram
from creds import Creds

from miscellaneous.locks import locks_fn

from yt_dl.yt_main import youtube
from miscellaneous.buttons import button_yt
from miscellaneous.executor import executor
from miscellaneous.miscellaneous import train, start, status, m_info, help_fn
from download.download import download_in_cmg
from gdrive.tg_doc import dl_doc
from gdrive.auth import auth, revoke, token


app = Client(
        "Hermes",
        bot_token=Creds.TG_TOKEN,
        api_id=Creds.APP_ID,
        api_hash=Creds.API_HASH,
        workers=343
    )

def install_ngrok():
    import os
    from zipfile import ZipFile
    from urllib.request import urlretrieve
    
    url = 'https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip'
    urlretrieve(url, 'ngrok-amd64.zip')
    
    with ZipFile('ngrok-amd64.zip', 'r') as zip_ref:
        zip_ref.extractall('/usr/local/bin/')
    os.chmod('/usr/local/bin/ngrok', 0o755)
    os.unlink('ngrok-amd64.zip')

app.add_handler(pyrogram.handlers.MessageHandler(install_ngrok,filters=filters.command(['ngrok'])))

#@app.on_message(filters.command(["qw"]))

#The gdrive auth handler
app.add_handler(pyrogram.handlers.MessageHandler(auth,filters=filters.command(['auth'])))

#The gdrive Revoke handler
app.add_handler(pyrogram.handlers.MessageHandler(revoke,filters=filters.command(['revoke'])))

#The handler for authenticating the token
app.add_handler(pyrogram.handlers.MessageHandler(token,filters=filters.regex(r'.\/.{55}')))

#The Start handler
app.add_handler(pyrogram.handlers.MessageHandler(start,filters=filters.command(['start'])))

#The status hander
app.add_handler(pyrogram.handlers.MessageHandler(status,filters=filters.command(['status'])))

#The lock and unlock handler
app.add_handler(pyrogram.handlers.MessageHandler(locks_fn,filters=filters.command(['lock'])))

#The executor Handler
app.add_handler(pyrogram.handlers.MessageHandler(executor,filters=filters.command(['exec'])))

#The message info handler --> .thread
app.add_handler(pyrogram.handlers.MessageHandler(m_info,filters=filters.command(['info'])))

#The help handler
app.add_handler(pyrogram.handlers.MessageHandler(help_fn,filters=filters.command(['help'])))

# The tg doc handler
app.add_handler(pyrogram.handlers.MessageHandler(dl_doc,filters=filters.document))

#The youtube handlers 
yt_regex = r"(?:https?:)?(?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtu\.be\/|youtube(?:-nocookie)?\.com\/\S*?[^\w\s-])((?!videoseries)[\w-]{11})(?=[^\w-]|$)(?![?=&+%\w.-]*(?:['\"][^<>]*>|<\/a>))[?=&+%\w.-]*"
app.add_handler(pyrogram.handlers.MessageHandler(youtube,filters=filters.regex(yt_regex)))
app.add_handler(pyrogram.handlers.MessageHandler(youtube,filters=filters.command(['yt'])))

#Thw button handler
app.add_handler(pyrogram.handlers.CallbackQueryHandler(button_yt))

#The download handler(upload to tg)
dl_regex = r"\bhttp[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.(?!com)[a-z0-9]{3,4}\b"
app.add_handler(pyrogram.handlers.MessageHandler(download_in_cmg,filters=filters.command(['upload'])))

#The hmm|mm handler
app.add_handler(pyrogram.handlers.MessageHandler(train,filters=filters.regex(r'\b[Hh]m+\b') | filters.regex(r'\b[Mm]{2,}\b')))



app.run()  # Automatically start() and idle()