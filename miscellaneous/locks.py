import time
import asyncio

locks = {
        'youtube' : True,
        'document' : True,
        'upload' : True,
        'revoke' : False,
        'auth' : True,
        'token' : True,
        'executor' : False,
        'train' : True
    }

def toogle_all(stat):
    for fn in locks.keys():
        locks[fn] = stat

def status_all():
    status = ""
    for x,y in locks.items():
        status += x + " : " + str(y) + "\n"
    return status

async def send_msg(message, text):
    a = await message.reply_text(text)
    await message.delete()
    await asyncio.sleep(5)
    await a.delete()

async def locks_fn(client, message):

    content = message.text.lower().split()[1:]

    if content[0] == 'status':
        if content[1] == 'all':
            await send_msg(message, status_all())
        else:
            await send_msg(message, content[1] + " : " + str(locks[content[1]]))

    elif content[0] == 'lock':
        if content[1] == 'all':
            toogle_all(False)
            await send_msg(message, status_all())
        else:
            locks[content[1]] = False
            await send_msg(message, content[1] + " : " + str(locks[content[1]]))
            
    elif content[0] == 'unlock':
        if content[1] == 'all':
            toogle_all(True)
            await send_msg(message, status_all())
        else:
            locks[content[1]] = True
            await send_msg(message, content[1] + " : " + str(locks[content[1]]))
    
    elif content[0] == 'help':
        commands = "\n".join([x for x in locks.keys()])
        await send_msg(message, commands)
        



