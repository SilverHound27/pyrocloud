from pyrogram import Client, Filters
from creds import Config

app = Client(
        "Spambot",
        bot_token=Config.TG_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
    )


@app.on_message(Filters.document)
def echo(client, message):
    print(123)
    message.reply_text('hi')
    

app.run()