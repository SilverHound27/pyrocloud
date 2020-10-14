from miscellaneous.locks import locks
from download.download_fn import smart_dl,wget_dl
from upload_helper.upload import upload_to_tg
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import re
url_ext_ed = ""
mkup = [[InlineKeyboardButton(text=' Upload to telegram ', callback_data=b'telegram')],
            [InlineKeyboardButton(text=' Generate faster link ', callback_data=b'gdrive')],
            [InlineKeyboardButton(text='Cancel', callback_data=b'exit')]]

rply_mkup = InlineKeyboardMarkup(mkup)

dl_regex = r"\bhttp[s]?:\/\/(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+\.(?!com)[a-z0-9]{3,4}\b"

async def download_in_cmg(client, message):

    if not locks['upload']:# or message.text.upper().endswith(".HTML", "PHP", ".HTM"):
        return
    global url_ext_ed
    try:
        url_ext_ed = re.search(dl_regex, message.text).group()
    except:
        try:
            url_ext_ed = message.reply_to_message.text
        except:
            url_ext_ed = None
    
    if url_ext_ed is not None:
        a = await message.reply(text ="detected URL:\n"+url_ext_ed , reply_markup = rply_mkup)
    else:
        a = await message.reply("Couldnt find a proper link")

async def download_fn(bot, update):
    upload_type = update.data

    if upload_type == 'exit':
        await update.message.delete()
        await update.message.reply_to_message.delete()
        return
    elif upload_type == 'gdrive':
        await update.message.edit("aa ayacha link thanne eduthu angu upayogicha mathi\n #coming_soon")
    elif upload_type == 'telegram':
        snd_msg = await update.message.edit("Processing "+ url_ext_ed)
        print("ID",update.from_user.id)
        dest_folder = await smart_dl(url_ext_ed, update)
        if dest_folder:
            user_id = update.from_user.id
        #
            final_response = await upload_to_tg(
                update.message,
                dest_folder,
                user_id,
                {},
                True
            )
