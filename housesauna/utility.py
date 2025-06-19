import os
import logging

from dotenv import load_dotenv
import telepot

load_dotenv()

logger = logging.getLogger(__name__)


my_token = os.getenv('TELEGRAM_TOKEN_PROD', '')

my_chat_id = os.getenv('TELEGRAM_CHAT_PROD', '')


def send_telegram(msg: str) -> None:
    """
    Отправка сообщения в телеграм.
    """
    logging.info(f'Сообщение для отправки в телеграм: {msg}')
    bot = telepot.Bot(my_token)
    bot.sendMessage(chat_id=my_chat_id, text=msg)
    logging.debug('Сообщение отправлено!')
