from requests import get
from math import ceil
from subprocess import Popen, PIPE
import wget
import datetime
import asyncio
#from __future__ import unicode_literals
import youtube_dl
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
import os


url = 'https://www.googleapis.com/youtube/v3/search?pageToken={}&key={}&channelId={}&part=snippet,id&order=date&maxResults=200'
key = 'AIzaSyBK3nG2HG-RxvY7Hl9zexYB2yXVPLvEqok'

yt_channel = ''
tg_channel = ""
vid_data = []


async def parse_data(data):
    if data['items'] == []:
        print('Invalid or empty channel')
        return

    for i in data['items']:
        try:
            video = 'https://www.youtube.com/watch?v=' + i['id']['videoId']
            title = i['snippet']['title']
            description = i['snippet']['description']
            date = i['snippet']['publishedAt']
            thumbnail = i['snippet']['thumbnails']['medium']['url']
            vid_data.append([video, title, thumbnail, date, description])
        except:
            continue


async def get_vid_list(pageToken=""):
    data = get(url.format(pageToken, key, yt_channel))
    data = data.json()
    await parse_data(data)
    #no_iterations = ceil(data['pageInfo']['totalResults']/50)
    pageToken = data.get('nextPageToken', False)
    if pageToken:
        await get_vid_list(pageToken)





async def upload_vid(client, filename, title, description, date, url):

    metadata = extractMetadata(createParser(filename))
    duration = 0
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds

    caption_str = f'<code><b>{title}</b></code>\n\n{description}\n\nUploaded date: {date}\n\n <a href ="{url}">YouTube Link</a>'

    await client.send_video(chat_id = tg_channel,
                             video = filename,
                             caption = caption_str,
                             parse_mode = 'html',
                             duration = duration,
                             width = 320,
                             height= 180,
                             thumb = 'thumbnail.jpg',
                             supports_streaming = True,
                             disable_notification=True)
    os.remove(filename)
    os.remove('thumbnail.jpg')

async def download_video(client, metadata):
    """accepts a list; downloads best quality available"""
    url,title,thumbnail_url,date,description = metadata
    filename = title+'.mp4'

    thumbnail = wget.download(thumbnail_url, out='thumbnail.jpg')

    ydl_opts = {'outtmpl': filename,
                'format': 'best'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    await upload_vid(client, filename, title, description, date, url)

        
async def ytchannel(client, message):
    '''input = command ytchannel password'''
    print(str(hash(str(datetime.datetime.now(datetime.timezone.utc))[:16]))[-5:])

    global tg_channel, yt_channel
    tg_channel = message.chat.id
    yt_channel = message.text.split()[-1]
    #yt_channel = "UCkitABalXafr-NqceQdDXtg"
    '''if password != str(hash(str(datetime.datetime.now(datetime.timezone.utc))[:16]))[-5:]:
        incorrect_pass = await message.reply_text('Incorrect password \n Make sure you have the correct password')
        await asyncio.sleep(10)
        await incorrect_pass.delete()'''


 
    await get_vid_list()
    for vid in vid_data:
        await download_video(client, vid)
        #await upload_vid(client, vid)
        print(vid)
        await asyncio.sleep(180)
#yt_channel(1,2)
