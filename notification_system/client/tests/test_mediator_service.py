import pytest
from ..mediator_service import MediatorService
from .factories.client_factory import ClientFactory
from ..exceptions import (
    SmsNotificationFailedException,
    EmailNotificationFailedException,
    TelegramNotificationFailedException,
    NoNotificationMethodException,
    NoTelegramException,
    NoPhoneException,
    NoEmailException
)


@pytest.mark.django_db
def test_mediator_service_with_incorrect_sms_sending(send_notification):
    send_notification.side_effect = Exception()
    client = ClientFactory()

    service = MediatorService(
        send_sms=send_notification,
        send_email=send_notification,
        telegram_bot=None,
        client=client,
    )
    with pytest.raises(SmsNotificationFailedException):
        service.send_sms_notification("test")


@pytest.mark.django_db
def test_mediator_service_with_incorrect_email_sending(send_notification):
    send_notification.side_effect = Exception()
    client = ClientFactory()

    service = MediatorService(
        send_sms=send_notification,
        send_email=send_notification,
        telegram_bot=None,
        client=client,
    )
    with pytest.raises(EmailNotificationFailedException):
        service.send_email_notification("test")


@pytest.mark.django_db
def test_mediator_service_with_incorrect_telegram_sending(telebot, send_notification):
    send_notification.side_effect = Exception()
    telebot.send_message.side_effect = Exception()
    client = ClientFactory()

    service = MediatorService(
        send_sms=send_notification,
        send_email=send_notification,
        telegram_bot=telebot,
        client=client,
    )
    with pytest.raises(TelegramNotificationFailedException):
        service.send_telegram_notification("test")


@pytest.mark.django_db
def test_mediator_service_with_empty_client(send_notification, telebot):
    client = ClientFactory()

    client.telegram_id = None
    client.phone = None
    client.email = None

    client.save()

    service = MediatorService(
        send_sms=send_notification,
        send_email=send_notification,
        telegram_bot=telebot,
        client=client,
    )
    with pytest.raises(NoNotificationMethodException):
        service.send_all_notifications(text="test")


@pytest.mark.django_db
def test_mediator_service_with_empty_telegram_id(send_notification, telebot):
    client = ClientFactory()
    client.telegram_id = None
    client.save()

    service = MediatorService(
        send_sms=send_notification,
        send_email=send_notification,
        telegram_bot=telebot,
        client=client,
    )
    with pytest.raises(NoTelegramException):
        service.send_telegram_notification("")


@pytest.mark.django_db
def test_mediator_service_with_empty_phone(send_notification, telebot):
    client = ClientFactory()
    client.phone = None
    client.save()

    service = MediatorService(
        send_sms=send_notification,
        send_email=send_notification,
        telegram_bot=telebot,
        client=client,
    )
    with pytest.raises(NoPhoneException):
        service.send_sms_notification("")

@pytest.mark.django_db
def test_mediator_service_with_empty_email(send_notification, telebot):
    client = ClientFactory()
    client.email = None
    client.save()

    service = MediatorService(send_sms=send_notification, send_email=send_notification, telegram_bot=telebot, client=client)
    with pytest.raises(NoEmailException):
        service.send_email_notification("")

@pytest.mark.django_db
def test_mediator_sends_correct_notifications(send_notification, telebot):
    client = ClientFactory()

    service = MediatorService(send_sms=send_notification, send_email=send_notification, telegram_bot=telebot, client=client)
    service.send_all_notifications("test")