from telegram.ext import ApplicationBuilder
import asyncio

TOKEN = '7859289535:AAGHHdzhp8LiFp-ZE0_AE4LRTzhLAnRyLT0'
CHAT_ID = 7983961143  # Твой чат ID


async def send_daily_photo():
    app = ApplicationBuilder().token(TOKEN).build()
    await app.initialize()
    await app.start()

    photo_url = 'https://w7.pngwing.com/pngs/234/329/png-transparent-python-logo-thumbnail.png'
    await app.bot.send_photo(chat_id=CHAT_ID, photo=photo_url, caption="Here's your daily photo!")

    await app.stop()


if __name__ == '__main__':
    asyncio.run(send_daily_photo())
