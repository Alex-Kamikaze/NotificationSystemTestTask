from typing import Protocol, List
from django.conf import settings
from .exceptions import SmsNotificationFailedException, EmailNotificationFailedException, TelegramNotificationFailedException

class SendMail(Protocol):
    pass

class SendSMS(Protocol):
    pass

class TelegramBot(Protocol):
    def send_message(user_id, text):
        pass

class SMSService:

    def __init__(self, send_sms: SendSMS):
        # Нужно для мока отправки смсок
        self.send_sms = send_sms

    def __call__(self, sender: str, receivers: List[str], text: str):
        self.__send_sms(sender=sender, text=text, receivers=receivers)

    def __send_sms(self, sender: str, receivers: List[str], text: str):
        try:
            self.send_sms(text, sender, receivers, fail_silently=False)
        except Exception as e:
            print(e)
            raise SmsNotificationFailedException()


class TelegramService:
    def __init__(self, bot: TelegramBot):
        # Нужно для мока класса бота
        self.bot = bot

    def __call__(self, user_id: int, message: str):
        self.__send_message(user_id, message)

    def __send_message(self, user_id: int, message: str):
        try:
            self.bot.send_message(user_id, text=message)
        except Exception:
            raise TelegramNotificationFailedException()


class EmailSendService:
    
    def __init__(self, send_mail: SendMail):
        # Нужно для мока отправки сообщений
        self.send_mail = send_mail

    def __call__(self, receiver: str, text: str):
        self.__send_email(receiver, text)

    def __send_email(self, receiver: str, text: str):
        try:
            self.send_mail(subject="Тестовое уведомление", from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=[receiver], message=text, fail_silently=False)
        except Exception as e:
            print(e)
            raise EmailNotificationFailedException()