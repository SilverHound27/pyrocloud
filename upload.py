#!/usr/bin/env python3
import argparse
import json
import os
import os.path as path
import re
from creds import Creds
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

FOLDER_MIME_TYPE = 'application/vnd.google-apps.folder'
drive: GoogleDrive
http = None
initial_folder = None


async def upload(filename: str, update, context, parent_folder: str = None) -> None:

    FOLDER_MIME_TYPE = 'application/vnd.google-apps.folder'
    drive: GoogleDrive
    http = None
    initial_folder = None
    gauth: drive.GoogleAuth = GoogleAuth()

    ID = update.chat.id
    ID = str(ID)
    gauth.LoadCredentialsFile(
        path.join(path.dirname(path.abspath(__file__)), ID))

    if gauth.credentials is None:
        print("not Auth Users")
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
        gauth.SaveCredentialsFile(
            path.join(path.dirname(path.abspath(__file__)), ID))
    else:
        # Initialize the saved creds
        gauth.Authorize()
    drive = GoogleDrive(gauth)
    http = drive.auth.Get_Http_Object()
    if not path.exists(filename):
        print(f"Specified filename {filename} does not exist!")
        return
    # print(filename)
    
    file_params = {'title': filename.split('/')[-1]}
    
    if Creds.TEAMDRIVE_FOLDER_ID :
        file_params['parents'] = [{"kind": "drive#fileLink", "teamDriveId": Creds.TEAMDRIVE_ID, "id":Creds.TEAMDRIVE_FOLDER_ID}]
    

    file_to_upload = drive.CreateFile(file_params)
    file_to_upload.SetContentFile(filename)

    try:
        print('Trying to upload', filename)
        file_to_upload.Upload(param={"supportsTeamDrives" : True , "http": http})
        print('upload completed')
        
    except Exception as e:
        print("upload",e)
        
    #return file_to_upload['webContentLink']
    return 'https://telegram.archives.workers.dev/{}'.format(filename)
