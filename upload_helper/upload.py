#!/usr/bin/env python3
import argparse
import json
import os
import os.path as path
import re
import time
from creds import Creds
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from progress import progress_for_pyrogram
from pyrogram.types import InputMediaVideo, InputMediaAudio
from miscellaneous.locks import locks

FOLDER_MIME_TYPE = 'application/vnd.google-apps.folder'
drive: GoogleDrive
http = None
initial_folder = None


async def server_upload(filename: str, update, context, parent_folder: str = None) -> None:
    if not locks['upload']:
        return

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
        
    return 'https://telegram.archives.workers.dev/{}'.format(filename)


########################################################################
########################################################################
########################################################################
import asyncio
import os
import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from PIL import Image
from progress import progress_for_pyrogram, humanbytes
from upload_helper.help_Nekmo_ffmpeg import take_screen_shot
from upload_helper.split_large_files import split_large_files
from upload_helper.copy_similar_file import copy_file

from creds import Creds
TG_MAX_FILE_SIZE = Creds.TG_MAX_FILE_SIZE
EDIT_SLEEP_TIME_OUT = Creds.EDIT_SLEEP_TIME_OUT
DOWNLOAD_LOCATION = Creds.DOWNLOAD_LOCATION

from pyrogram.types import (
    InputMediaDocument,
    InputMediaVideo,
    InputMediaAudio
)


async def upload_to_tg(
    message,
    local_file_name,
    from_user,
    dict_contatining_uploaded_files,
    edit_media=False
):
    if not locks['upload']:
        return

    base_file_name = os.path.basename(local_file_name)
    caption_str = ""
    caption_str += "<code>"
    caption_str += base_file_name
    caption_str += "</code>"
    # caption_str += "\n\n"
    # caption_str += "<a href='tg://user?id="
    # caption_str += str(from_user)
    # caption_str += "'>"
    # caption_str += "Here is the file to the link you sent"
    # caption_str += "</a>"
    if os.path.isdir(local_file_name):
        directory_contents = os.listdir(local_file_name)
        directory_contents.sort()
        # number_of_files = len(directory_contents)
        new_m_esg = message
        if not message.photo:
            new_m_esg = await message.reply_text(
                "Found {} files".format(len(directory_contents)),
                quote=True
                # reply_to_message_id=message.message_id
            )
        for single_file in directory_contents:
            # recursion: will this FAIL somewhere?
            await upload_to_tg(
                new_m_esg,
                os.path.join(local_file_name, single_file),
                from_user,
                dict_contatining_uploaded_files,
                edit_media
            )
    else:
        if os.path.getsize(local_file_name) > TG_MAX_FILE_SIZE:
            d_f_s = humanbytes(os.path.getsize(local_file_name))
            i_m_s_g = await message.reply_text(
                "File too heavy.\n"
                f"Detected File Size: {d_f_s} \n"
                "\n splitting files..."
            )
            splitted_dir = await split_large_files(local_file_name)
            totlaa_sleif = os.listdir(splitted_dir)
            totlaa_sleif.sort()
            number_of_files = len(totlaa_sleif)
            ba_se_file_name = os.path.basename(local_file_name)
            await i_m_s_g.edit_text(
                f"File Size: {d_f_s} \n"
                f"<code>{ba_se_file_name}</code> will be split into {number_of_files} files.\n"
                "upload in progress..."
            )
            for le_file in totlaa_sleif:
                # recursion: will this FAIL somewhere?
                await upload_to_tg(
                    message,
                    os.path.join(splitted_dir, le_file),
                    from_user,
                    dict_contatining_uploaded_files
                )
        else:
            sent_message = await upload_single_file(
                message,
                local_file_name,
                caption_str,
                from_user,
                edit_media
            )
            if sent_message is not None:
                dict_contatining_uploaded_files[os.path.basename(local_file_name)] = sent_message.message_id
    # await message.delete()
    return dict_contatining_uploaded_files


async def upload_single_file(message, local_file_name, caption_str, from_user, edit_media):
    print('file uploahing rn:', local_file_name)
    
    await asyncio.sleep(EDIT_SLEEP_TIME_OUT)
    sent_message = None
    start_time = time.time()
    #
    thumbnail_location = os.path.join(
        DOWNLOAD_LOCATION,
        "thumbnails",
        str(from_user) + ".jpg"
    )
    #
    try:
        message_for_progress_display = message
        if not edit_media:
            message_for_progress_display = await message.reply_text(
                "starting upload of {}".format(os.path.basename(local_file_name))
            )
        if local_file_name.upper().endswith(("MKV", "MP4", "WEBM")):
            metadata = extractMetadata(createParser(local_file_name))
            duration = 0
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            #
            width = 0
            height = 0
            thumb_image_path = None
            if os.path.exists(thumbnail_location):
                thumb_image_path = await copy_file(
                    thumbnail_location,
                    os.path.dirname(os.path.abspath(local_file_name))
                )
            else:
                thumb_image_path = await take_screen_shot(
                    local_file_name,
                    os.path.dirname(os.path.abspath(local_file_name)),
                    (duration / 2)
                )
                # get the correct width, height, and duration for videos greater than 10MB
                if os.path.exists(thumb_image_path):
                    metadata = extractMetadata(createParser(thumb_image_path))
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                    # resize image
                    # ref: https://t.me/PyrogramChat/44663
                    # https://stackoverflow.com/a/21669827/4723940
                    Image.open(thumb_image_path).convert(
                        "RGB"
                    ).save(thumb_image_path)
                    img = Image.open(thumb_image_path)
                    # https://stackoverflow.com/a/37631799/4723940
                    img.resize((320, height))
                    img.save(thumb_image_path, "JPEG")
                    # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
            #'''
            thumb = None
            if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                thumb = thumb_image_path
            # send video
            if edit_media and message.photo:
                sent_message = await message.edit_media(
                    media=InputMediaVideo(
                        media=local_file_name,
                        thumb=thumb,
                        caption=caption_str,
                        parse_mode="html",
                        width=width,
                        height=height,
                        duration=duration,
                        supports_streaming=True
                    )
                    # quote=Tredit_mediaue,
                )
            else:
                sent_message = await message.reply_video(
                    video=local_file_name,
                    # quote=True,
                    caption=caption_str,
                    parse_mode="html",
                    duration=duration,
                    width=width,
                    height=height,
                    thumb=thumb,
                    supports_streaming=True,
                    disable_notification=True,
                    #reply_to_message_id=message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "trying to upload",
                        message_for_progress_display,
                        start_time
                    )
                )
            if thumb is not None:
                os.remove(thumb)
        elif local_file_name.upper().endswith(("MP3", "M4A", "M4B", "FLAC", "WAV")):
            metadata = extractMetadata(createParser(local_file_name))
            duration = 0
            title = ""
            artist = ""
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            if metadata.has("title"):
                title = metadata.get("title")
            if metadata.has("artist"):
                artist = metadata.get("artist")
            thumb_image_path = None
            if os.path.isfile(thumbnail_location):
                thumb_image_path = await copy_file(
                    thumbnail_location,
                    os.path.dirname(os.path.abspath(local_file_name))
                )
            thumb = None
            if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                thumb = thumb_image_path
            # send audio
            if edit_media and message.photo:
                sent_message = await message.edit_media(
                    media=InputMediaAudio(
                        media=local_file_name,
                        thumb=thumb,
                        caption=caption_str,
                        parse_mode="html",
                        duration=duration,
                        performer=artist,
                        title=title
                    )
                    # quote=True,
                )
            else:
                sent_message = await message.reply_audio(
                    audio=local_file_name,
                    # quote=True,
                    caption=caption_str,
                    parse_mode="html",
                    duration=duration,
                    performer=artist,
                    title=title,
                    thumb=thumb,
                    disable_notification=True,
                    #reply_to_message_id=message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "trying to upload",
                        message_for_progress_display,
                        start_time
                    )
                )
            if thumb is not None:
                os.remove(thumb)
        
        else:
            thumb_image_path = None
            if os.path.isfile(thumbnail_location):
                thumb_image_path = await copy_file(
                    thumbnail_location,
                    os.path.dirname(os.path.abspath(local_file_name))
                )
            # if a file, don't upload "thumb"
            # this "diff" is a major derp -_- 😔😭😭
            thumb = None
            if thumb_image_path is not None and os.path.isfile(thumb_image_path):
                thumb = thumb_image_path
            #
            # send document
            if edit_media and message.photo:
                sent_message = await message.edit_media(
                    media=InputMediaDocument(
                        media=local_file_name,
                        thumb=thumb,
                        caption=caption_str,
                        parse_mode="html"
                    )
                    # quote=True,
                )
            else:
                sent_message = await message.reply_document(
                    document=local_file_name,
                    # quote=True,
                    thumb=thumb,
                    caption=caption_str,
                    parse_mode="html",
                    disable_notification=True,
                    reply_to_message_id=message.reply_to_message.message_id,
                    progress=progress_for_pyrogram,
                    progress_args=(
                        "trying to upload",
                        message_for_progress_display,
                        start_time
                    )
                )
            if thumb is not None:
                os.remove(thumb)

        #####POTENTIAL bug
        try:
            await message.delete()
            #await message.reply_to_message.delete()
        except:
            pass

    except Exception as e:
        await message_for_progress_display.edit_text("**FAILED**\n" + str(e))
    else:
        if message.message_id != message_for_progress_display.message_id:
            await message_for_progress_display.delete()
    os.remove(local_file_name)
    print('done')
    return sent_message
