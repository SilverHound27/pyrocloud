from yt_dl.youtube_dl_button import youtube_dl_call_back
from download.download import download_fn

async def button_yt(bot, update):
    cb_data = update.data
    
    if "|" in cb_data:
        await youtube_dl_call_back(bot, update)

    elif 'grive' or 'telegram' or 'exit':
        await download_fn(bot, update)