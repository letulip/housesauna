import os

from dotenv import load_dotenv
import telepot

load_dotenv()


my_token = os.getenv('TELEGRAM_TOKEN_PROD', '')

my_chat_id = os.getenv('TELEGRAM_CHAT_PROD', '')


def send_telegram(msg: str) -> None:
    """
    Send a message to a telegram user or group specified on chatId
    chat_id must be a number!
    """
    print(msg)
    bot = telepot.Bot(my_token)
    bot.sendMessage(chat_id=my_chat_id, text=msg)
