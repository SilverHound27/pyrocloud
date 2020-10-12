import re
import os
from yt_dl.youtube_dl_extractor import extract_youtube_dl_formats
from miscellaneous.locks import locks

DOWNLOAD_LOCATION = os.getcwd()
yt_regex = r"(?:https?:)?(?:\/\/)?(?:[0-9A-Z-]+\.)?(?:youtu\.be\/|youtube(?:-nocookie)?\.com\/\S*?[^\w\s-])((?!videoseries)[\w-]{11})(?=[^\w-]|$)(?![?=&+%\w.-]*(?:['\"][^<>]*>|<\/a>))[?=&+%\w.-]*"




async def youtube(client, message):
    if not locks['youtube']:
        return
        
    i_m_sefg = await message.reply_text("processing", quote=True)

    try:
        url_ext_ed = re.search(yt_regex, message.text).group()
    except:
        try:
            url_ext_ed = message.reply_to_message.text
        except:
            url_ext_ed = None


    dl_url, cf_name, yt_dl_user_name, yt_dl_pass_word = url_ext_ed, None, None, None
    
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        current_user_id = message.from_user.id

        user_working_dir = os.path.join(DOWNLOAD_LOCATION, str(current_user_id))
        if not os.path.isdir(user_working_dir):
            os.makedirs(user_working_dir)

        thumb_image, text_message, reply_markup = await extract_youtube_dl_formats(dl_url,yt_dl_user_name,yt_dl_pass_word,user_working_dir)
        
        if thumb_image is not None:
            await message.reply_photo(photo=thumb_image,quote=True,caption=text_message,reply_markup=reply_markup)
            await i_m_sefg.delete()
        else:
            await i_m_sefg.edit_text(text=text_message, reply_markup=reply_markup)
    else:
        i = await i_m_sefg.edit("Couldn't find a valid link")