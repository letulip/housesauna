import os
from datetime import datetime
import smtplib
import socket

from django.conf import settings
from django.core.mail import send_mail
import telepot
from telepot.exception import TelegramError, BadHTTPResponse
from housesauna.logger import logger


TOKEN_TG = os.getenv('TELEGRAM_TOKEN_PROD', '')
CHAT_ID_TG = os.getenv('TELEGRAM_CHAT_PROD', '')


def send_telegram(msg: str) -> None:
    """
    Отправка сообщения в телеграм.
    """
    try:
        bot = telepot.Bot(TOKEN_TG)
        bot.sendMessage(chat_id=CHAT_ID_TG, text=msg)
        logger.info(f'[Telegram] Отправлено: {msg}')
    except (TelegramError, BadHTTPResponse) as e:
        logger.warning(f'[Telegram] Ошибка: {e}')
        logger.warning(f'[Telegram] Сообщение не отправлено: {msg}')
        raise


def send_email_notification(subject, message, sender, recipients):
    """
    Отправка сообщения на почту.
    Кастомное логирование с исключением.
    """
    try:
        send_mail(subject, message, sender, recipients)
        logger.info(f'[Email] Отправлено сообщение: {message}')
    except (
        smtplib.SMTPException,
        socket.error,
        UnicodeEncodeError,
        ConnectionRefusedError,
        TimeoutError
    ) as e:
        logger.warning(f'[Email] Ошибка: {e}')
        logger.warning(f'[Email] Сообщение не отправлено: {message}')
        raise


def save_failed_submission(data: dict):
    """
    Сохраняет данные неотправленной заявки в один лог-файл.
    """
    file_name = 'failed_submissions.log'
    file_path = os.path.join(settings.LOG_DIR, file_name)
    logger.info(f'Добавляется запись в файл: {file_path}')

    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f'=== Заявка от {timestamp} ===\n')
            for key, value in data.items():
                f.write(f'{key}: {value}\n')
            f.write('\n')
            logger.info('Неотправленная заявка сохранена.')
    except Exception as e:
        logger.error(f'Не удалось сохранить заявку: {e}')
