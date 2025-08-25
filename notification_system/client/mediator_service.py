from dataclasses import dataclass
from django.conf import settings
from .send_services import (
    SMSService,
    EmailSendService,
    TelegramService,
    SendSMS,
    SendMail,
    TelegramBot,
)
from .models import Client
from .exceptions import (
    NoEmailException,
    EmailNotificationFailedException,
    NoPhoneException,
    SmsNotificationFailedException,
    NoTelegramException,
    TelegramNotificationFailedException,
    NoNotificationMethodException
)

@dataclass
class NotificationResults:
    telegram: bool = True
    email: bool = True
    sms: bool = True



class MediatorService:
    def __init__(
        self,
        send_sms: SendSMS,
        send_email: SendMail,
        telegram_bot: TelegramBot,
        client: Client,
    ):
        self.sms_service = SMSService(send_sms)
        self.email_service = EmailSendService(send_email)
        self.telegram_bot_service = TelegramService(telegram_bot)
        self.client = client

    def send_email_notification(self, text: str):
        if not self.client.email:
            raise NoEmailException(
                message="У клиента не указан Email для отправки уведомления"
            )

        try:
            self.email_service(self.client.email, text)
        except Exception:
            raise EmailNotificationFailedException()

    def send_sms_notification(self, text: str):
        if not self.client.phone:
            raise NoPhoneException()

        try:
            self.sms_service(
                sender=settings.SMS_SENDER, receivers=[self.client.phone], text=text
            )
        except Exception:
            raise SmsNotificationFailedException()

    def send_telegram_notification(self, text: str):
        if not self.client.telegram_id:
            raise NoTelegramException()

        try:
            self.telegram_bot_service(self.client.telegram_id, text)
        except Exception:
            raise TelegramNotificationFailedException()
        
    def send_all_notifications(self, text: str) -> NotificationResults:
        results = NotificationResults()
        if not any([self.client.email, self.client.phone, self.client.telegram_id]):
            raise NoNotificationMethodException()
        
        try:
            self.email_service(self.client.email, text)
        except EmailNotificationFailedException:
            results.email = False

        try:
            self.sms_service(settings.SMS_SENDER, [self.client.phone], text)
        except SmsNotificationFailedException:
            results.sms = False

        try:
            self.telegram_bot_service(self.client.telegram_id, text)
        except TelegramNotificationFailedException:
            results.telegram = False

        return results