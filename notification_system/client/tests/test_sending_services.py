import pytest
from django.conf import settings
from client.send_services import SMSService, EmailSendService, TelegramService
from client.exceptions import SmsNotificationFailedException, EmailNotificationFailedException, TelegramNotificationFailedException

def test_sms_service_raises_exception(send_notification):
    send_notification.side_effect = Exception() # Имитируем выброс любого исключения с любого бекенда django-sms

    service = SMSService(send_notification)
    with pytest.raises(SmsNotificationFailedException):
        service(sender="+11111111111", receivers=["+2716161287317"], text="test")

def test_sms_service_sends_correctly(send_notification):
    service = SMSService(send_notification)
    service("+1111111", receivers=["+716161515"], text="test")

def test_email_service_raises_exception(send_notification):
    send_notification.side_effect = Exception() # Имитируем исключение при отправке сообщения
    service = EmailSendService(send_notification)

    with pytest.raises(EmailNotificationFailedException):
        service("test@gmail.com", "test")

def test_email_sent_correctly(send_notification):
    service = EmailSendService(send_notification)
    service(receiver="sashagameac@gmail.com", text="test")

def test_telegram_service_raises_exception(telebot):
    telebot.send_message.side_effect = Exception() # Имитируем ошибку со стороны телеграмма

    service = TelegramService(telebot)
    with pytest.raises(TelegramNotificationFailedException):
        service(0, "test")

def test_telegram_service_sends_correctly(telebot):
    service = TelegramService(telebot)
    service(0, "test")