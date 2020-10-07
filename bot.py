from pyrogram import Client, Filters
from creds import Creds
from random import randint
from progress import progress_for_pyrogram
import time
from pydrive.auth import GoogleAuth
from upload import upload
import os
gauth = GoogleAuth()


app = Client(
        "new",
        bot_token=Creds.TG_TOKEN,
        api_id=Creds.APP_ID,
        api_hash=Creds.API_HASH,
    )
@app.on_message(Filters.command(["auth"]))
def auth(client, message):
    FOLDER_MIME_TYPE = 'application/vnd.google-apps.folder'
    drive: GoogleDrive
    http = None
    initial_folder = None
    ID = message.chat.id
    ID = str(ID)
    try:
        gauth.LoadCredentialsFile(ID)
    except Exception as e:
        print("Cred file missing :", e)

    if gauth.credentials is None:
        authurl = gauth.GetAuthUrl()
        AUTH_URL = '<a href ="{}">Vist This Url</a> \n Generate And Copy Your Google Drive Token And Send It To Me'
        AUTH = AUTH_URL.format(authurl)
        message.reply_text(text=AUTH, parse_mode="html")

    elif gauth.access_token_expired:
        # Refresh Token if expired
        gauth.Refresh()
    else:
        # auth with  saved creds
        gauth.Authorize()
        message.reply_text("Already AUTH")



@app.on_message(Filters.text)
def token(client, message):
    msg = message.text
    ID = message.chat.id
    ID = str(ID)
    token = msg.split()[-1]
    if len(token) == 57 and token[1] == "/" :
        print(token)
        try:
            gauth.Auth(token)
            gauth.SaveCredentialsFile(ID)
            message.reply_text("AUTH Success")
        except Exception as e:
            print("Auth Error :", e)
            message.reply_text("AUTH Failed")
   
@app.on_message(Filters.command(["start"]))
def start(client, message):
    message.reply_text('HELLO WORLD')

@app.on_message(Filters.command(["status"]))
def alive(client, message):
    message.reply_text("I'm alive :)")





@app.on_message(Filters.document)
def echo(client, message):
    a = message.reply_text('doc found')
    c_time = time.time()
    file_name = ".".join(message.document.file_name.split())
    temp_name = os.path.join(os.getcwd(), file_name)
    file_path = client.download_media(message= message,
                    file_name = temp_name,
                    progress=progress_for_pyrogram,
                    progress_args=("Starting dl", a, c_time )
                    )
    
    a.edit(text = 'Trying to upload file: \n\t{}'.format(file_name))
    
    try:
        dl_url = upload(file_name, message, client, 'HERMES_UPLOAD')
    except Exception as e:
        print("error Code : UPX11", e)
        a.edit("Uploading fail :{}".format(e))
    else:
        a.edit("File uploaded successfully\n Filename: {}\n URL: {}".format(file_name, dl_url))
    try:
        os.remove(file_name)
    except Exception as e:
        print(e)
app.run()  # Automatically start() and idle()