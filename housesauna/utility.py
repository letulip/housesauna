import os
import logging
from datetime import datetime

from dotenv import load_dotenv
from django.conf import settings
from django.core.mail import send_mail
import telepot

load_dotenv()

logger = logging.getLogger(__name__)


my_token = os.getenv('TELEGRAM_TOKEN_PROD', '')

my_chat_id = os.getenv('TELEGRAM_CHAT_PROD', '')


def send_telegram(msg: str) -> None:
    """
    Отправка сообщения в телеграм.
    """
    try:
        bot = telepot.Bot(my_token)
        bot.sendMessage(chat_id=my_chat_id, text=msg)
        logger.info(f'[Telegram] Отправлено: {msg}')
    except Exception as e:
        logger.warning(f'[Telegram] Ошибка: {e}')
        logger.warning(f'[Telegram] Сообщение не отправлено: {msg}')


def send_email_notification(subject, message, sender, recipients):
    """
    Отправка сообщения на почту.
    Кастомное логирование с исключением.
    """
    try:
        send_mail(subject, message, sender, recipients)
        logger.info(f'[Email] Отправлено сообщение: {message}')
    except Exception as e:
        logger.warning(f'[Email] Ошибка: {e}')
        logger.warning(f'[Email] Сообщение не отправлено: {message}')


def save_failed_submission(data: dict):
    """
    Сохраняет данные заявки в файл, если ни телега, ни email не сработали.
    """
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_name = f'failed_submission_{timestamp}.txt'
    save_dir = os.path.join(settings.BASE_DIR, 'failed_submissions')
    os.makedirs(save_dir, exist_ok=True)

    file_path = os.path.join(save_dir, file_name)
    logger.info(f"Сохраняю файл по пути: {file_path}")

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('Неотправленная заявка:\n')
            for key, value in data.items():
                f.write(f"{key}: {value}\n")
    except Exception as e:
        logger.error(f"Не удалось сохранить файл заявки: {e}")
