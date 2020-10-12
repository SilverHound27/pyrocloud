import asyncio
from miscellaneous.locks import locks

async def executor(client, message):

    if not locks['executor']:
        return

    command_to_exec = message.text.split()[1:]
    command_reply = '<bold>Input Command:</bold>\n\t <code>{}</code> \n'.format(" ".join(command_to_exec))
    reply = await message.reply_text(command_reply, parse_mode="html")

    process = await asyncio.create_subprocess_exec(
        *command_to_exec,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,)

    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    print(t_response)
    error_reply = '<bold>Errors found:</bold> \n <code>{}</code> \n'.format(e_response)
    response_reply = "<bold>Response found:</bold> \n <code>{}</code>".format(t_response)
    
    n_reply = await reply.edit(command_reply + error_reply + response_reply, parse_mode="html")