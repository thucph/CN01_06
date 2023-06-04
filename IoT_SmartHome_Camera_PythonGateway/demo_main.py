import telegram
import asyncio
bot = telegram.Bot(token='5981765791:AAFt5RjPEgxXj5pk1Dh9xmrbnoM9HBtMDwc')
chat_id = '6075039245'

async def send_telegram_message():
    message = 'This is a test message!'
    try:
        await bot.send_message(chat_id=chat_id, text=message)
        print("Message sent successfully!")
    except Exception as e:
        print("Error sending message:", e)

asyncio.run(send_telegram_message())
