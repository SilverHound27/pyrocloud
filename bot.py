from pyrogram import Client, filters
import pyrogram
from creds import Creds
from progress import progress_for_pyrogram
import time
from pydrive.auth import GoogleAuth
from upload import server_upload
from yt_dl.yt_main import youtube
import os
from decoretors.buttons import button

gauth = GoogleAuth()


app = Client(
        "new",
        bot_token=Creds.TG_TOKEN,
        api_id=Creds.APP_ID,
        api_hash=Creds.API_HASH,
    )
@app.on_message(filters.command(["auth"]))
async def auth(client, message):
    FOLDER_MIME_TYPE = 'application/vnd.google-apps.folder'
    drive: GoogleDrive
    http = None
    initial_folder = None
    ID = str(message.chat.id)
    try:
        gauth.LoadCredentialsFile(ID)
    except Exception as e:
        print("Cred file missing :", e)

    if gauth.credentials is None:
        authurl = gauth.GetAuthUrl()
        AUTH_URL = '<a href ="{}">Vist This Url</a> \n Generate And Copy Your Google Drive Token And Send It To Me'
        AUTH = AUTH_URL.format(authurl)
        await message.reply_text(text=AUTH, parse_mode="html")

    elif gauth.access_token_expired:
        # Refresh Token if expired
        gauth.Refresh()
    else:
        # auth with  saved creds
        gauth.Authorize()
        await message.reply_text("Already AUTH")

@app.on_message(filters.command(["revoke"]))
def revoke(client, message):
    ID = str(message.chat.id)
    if os.path.isfile(ID):
        os.remove(ID)
        message.reply_text("Revoke Successful")
    else:
        message.reply_text("Ha Ha Ha")


@app.on_message(filters.regex(".\/.{55}"))
async def token(client, message):
    msg = message.text
    print(msg)
    ID = message.chat.id
    ID = str(ID)
    token = msg.split()[-1]
    if len(token) == 57 and token[1] == "/" :
        print(token)
        try:
            gauth.Auth(token)
            gauth.SaveCredentialsFile(ID)
            await message.reply_text("AUTH Success")
        except Exception as e:
            print("Auth Error :", e)
            await message.reply_text("AUTH Failed")
   
@app.on_message(filters.command(["start"]))
def start(client, message):
    message.reply_text('HELLO WORLD')

@app.on_message(filters.command(["status"]))
def alive(client, message):
    message.reply_text("I'm alive :)")

#\b[Hh]m+\b
@app.on_message(filters.regex(r'\b[Hh]m+\b') | filters.regex(r'\bm{2,}\b'))
def my_handler(client, message):
    message.reply_sticker("CAADAgADKAMAArVx2gaQekqHXpVKbhYE")


@app.on_message(filters.document)
async def echo(client, message):
    a = await message.reply_text('doc found')
    c_time = time.time()
    file_name = ".".join(message.document.file_name.split())
    temp_name = os.path.join(os.getcwd(), file_name)
    file_path = await client.download_media(message= message,
                    file_name = temp_name,
                    progress=progress_for_pyrogram,
                    progress_args=("Starting dl", a, c_time )
                    )
    
    await a.edit(text = 'Trying to upload file: \n\t{}'.format(file_name))
    
    print('Going into the upload function')
    dl_url = await server_upload(file_name, message, client, 'HERMES_UPLOAD')
    if not dl_url:
        await a.edit("Uploading failed")
    else:
        await a.edit('<code>{}</code> \n\t\t <a href ="{}">--DOWNLOAD--</a> \t\t\t\t#uploads'.format(file_name, dl_url))
        print('Final message: Upload success')
    if os.path.isfile(file_name):
        os.remove(file_name)
        print('file removed')

yt_regex = r"(?:https?:)?(?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtu\.be\/|youtube(?:-nocookie)?\.com\/\S*?[^\w\s-])((?!videoseries)[\w-]{11})(?=[^\w-]|$)(?![?=&+%\w.-]*(?:['\"][^<>]*>|<\/a>))[?=&+%\w.-]*"
app.add_handler(pyrogram.handlers.MessageHandler(youtube,filters=filters.regex(yt_regex)))
app.add_handler(pyrogram.handlers.CallbackQueryHandler(button))
 
app.run()  # Automatically start() and idle()