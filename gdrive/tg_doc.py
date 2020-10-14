import time
import os
from progress import progress_for_pyrogram
from upload_helper.upload import server_upload
from miscellaneous.locks import locks

async def dl_doc(client, message):
    if not locks['document']:
        return

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