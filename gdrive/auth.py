import os 
from pydrive.auth import GoogleAuth
from miscellaneous.locks import locks
gauth = GoogleAuth()

async def auth(client, message):
    if not locks['auth']:
        return
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

def revoke(client, message):
    if not locks['revoke']:
        return
    ID = str(message.chat.id)
    if os.path.isfile(ID):
        os.remove(ID)
        message.reply_text("Revoke Successful")
    else:
        message.reply_text("Ha Ha Ha")

async def token(client, message):
    if not locks['token']:
        return
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