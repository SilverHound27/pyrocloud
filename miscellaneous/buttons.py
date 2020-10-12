from yt_dl.youtube_dl_button import youtube_dl_call_back

async def button(bot, update):
    #print(update, '\n'*5, bot)
    cb_data = update.data
    if "|" in cb_data:
        await youtube_dl_call_back(bot, update)
    

