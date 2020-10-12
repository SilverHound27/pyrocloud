from pyrogram import Client, filters
import pyrogram
from creds import Creds


from yt_dl.yt_main import youtube
from miscellaneous.buttons import button
from miscellaneous.executor import executor
from miscellaneous.miscellaneous import train, start, status, m_info
from gdrive.tg_doc import dl_doc
from gdrive.auth import auth, revoke, token



mkup = [[pyrogram.types.InlineKeyboardButton(text=' Upload to telegram ', callback_data=b'telegram')],
            [pyrogram.types.InlineKeyboardButton(text=' Generate link ', callback_data=b'gdrive')]]
rply_mkup = pyrogram.types.InlineKeyboardMarkup(mkup)


app = Client(
        "Hermes",
        bot_token=Creds.TG_TOKEN,
        api_id=Creds.APP_ID,
        api_hash=Creds.API_HASH,
    )

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

#The executor Handler
app.add_handler(pyrogram.handlers.MessageHandler(executor,filters=filters.command(['exec'])))

#The message info handler --> .thread
app.add_handler(pyrogram.handlers.MessageHandler(m_info,filters=filters.command(['info'])))

# The tg doc handler
app.add_handler(pyrogram.handlers.MessageHandler(dl_doc,filters=filters.document))

#The youtube handlers 
yt_regex = r"(?:https?:)?(?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtu\.be\/|youtube(?:-nocookie)?\.com\/\S*?[^\w\s-])((?!videoseries)[\w-]{11})(?=[^\w-]|$)(?![?=&+%\w.-]*(?:['\"][^<>]*>|<\/a>))[?=&+%\w.-]*"
app.add_handler(pyrogram.handlers.MessageHandler(youtube,filters=filters.regex(yt_regex)))
app.add_handler(pyrogram.handlers.MessageHandler(youtube,filters=filters.command(['yt'])))

#Thw button handler
app.add_handler(pyrogram.handlers.CallbackQueryHandler(button))

#The hmm|mm handler
app.add_handler(pyrogram.handlers.MessageHandler(train,filters=filters.regex(r'\b[Hh]m+\b') | filters.regex(r'\bm{2,}\b')))


app.run()  # Automatically start() and idle()