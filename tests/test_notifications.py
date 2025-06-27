import pytest
from unittest.mock import patch, MagicMock
from housesauna.utility import send_telegram, send_email_notification


@pytest.mark.django_db
@patch('housesauna.utility.telepot.Bot')
def test_send_telegram_success(mock_bot_class):
    """sendMessage() вызывается правильно."""
    mock_bot = MagicMock()
    mock_bot_class.return_value = mock_bot

    send_telegram("Test message")

    mock_bot.sendMessage.assert_called_once()
    args, kwargs = mock_bot.sendMessage.call_args
    assert kwargs["text"] == "Test message"


@pytest.mark.django_db
@patch('housesauna.utility.telepot.Bot', side_effect=Exception("Telegram error"))
def test_send_telegram_failure(mock_bot_class, caplog):
    """Ошибка логируется."""
    with caplog.at_level("WARNING"):
        send_telegram("Test failure")
        assert "[Telegram] Ошибка: Telegram error" in caplog.text
        assert "Сообщение не отправлено: Test failure" in caplog.text


@pytest.mark.django_db
@patch('housesauna.utility.send_mail')
def test_send_email_notification_success(mock_send_mail, caplog):
    """send_mail() вызывается."""
    send_email_notification("Subject", "Body", "from@example.com", ["to@example.com"])
    mock_send_mail.assert_called_once()
    assert "[Email] Отправлено сообщение: Body" in caplog.text


@pytest.mark.django_db
@patch('housesauna.utility.send_mail', side_effect=Exception("Email error"))
def test_send_email_notification_failure(mock_send_mail, caplog):
    """Ошибка логируется при сбое."""
    with caplog.at_level("WARNING"):
        send_email_notification("Subject", "Body", "from@example.com", ["to@example.com"])
        assert "[Email] Ошибка: Email error" in caplog.text
        assert "Сообщение не отправлено: Body" in caplog.text
