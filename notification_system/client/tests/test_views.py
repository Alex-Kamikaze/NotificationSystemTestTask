import pytest
import json
from .factories.client_factory import ClientFactory
from ..mediator_service import MediatorService
from .. import views
from ..exceptions import SmsNotificationFailedException, TelegramNotificationFailedException, EmailNotificationFailedException

@pytest.mark.django_db
def test_incorrect_request_is_sent(api_client):
    resp = api_client.post("/notifications/send-all", data={"client_id": 1})
    assert resp.status_code == 400

    resp = api_client.post("/notifications/send-sms", data={"client_id": 1})
    assert resp.status_code == 400

    resp = api_client.post("/notifications/send-email", data={"client_id": 1})
    assert resp.status_code == 400

    resp = api_client.post("/notifications/send-telegram-message", data={"client_id": 1})
    assert resp.status_code == 400

@pytest.mark.django_db
def test_404_raises_if_client_not_in_db(api_client):
    resp = api_client.post("/notifications/send-all", data={"client_id": 1000, "text": "Hello"})
    assert resp.status_code == 404

    resp = api_client.post("/notifications/send-sms", data={"client_id": 1000, "text": "Hello"})
    assert resp.status_code == 404

    resp = api_client.post("/notifications/send-email", data={"client_id": 1000, "text": "Hello"})
    assert resp.status_code == 404

    resp = api_client.post("/notifications/send-telegram-message", data={"client_id": 1000, "text": "Hello"})
    assert resp.status_code == 404

@pytest.mark.django_db
def test_400_raises_if_no_notification_methods_are_availible(api_client):
    client = ClientFactory()
    client.telegram_id = None
    client.phone = None
    client.email = None
    client.save()

    resp = api_client.post("/notifications/send-all", data={"client_id": client.pk, "text": "hello"})
    assert resp.status_code == 400

@pytest.mark.django_db
def test_raises_400_if_client_has_no_phone(api_client):
    client = ClientFactory()
    client.phone = None
    client.save()

    resp = api_client.post("/notifications/send-sms", data={"client_id": client.pk, "text": "hello"})
    assert resp.status_code == 400

@pytest.mark.django_db
def test_raises_503_if_sms_is_not_sent(api_client, send_notification, telebot, monkeypatch, mocker):
    client = ClientFactory()
    send_sms_mock = mocker.MagicMock()
    send_sms_mock.side_effect = SmsNotificationFailedException

    monkeypatch.setattr(views, "send_sms", send_sms_mock)

    resp = api_client.post("/notifications/send-sms", data={"client_id": client.pk, "text": "hello"})
    assert resp.status_code == 503

@pytest.mark.django_db
def test_raises_400_if_client_has_no_telegram_id(api_client):
    client = ClientFactory()
    client.telegram_id = None
    client.save()

    resp = api_client.post("/notifications/send-telegram-message", data={"client_id": client.pk, "text": "Hello"})
    assert resp.status_code == 400

@pytest.mark.django_db
def test_raises_503_if_telegram_message_is_not_sent(api_client, monkeypatch, mocker):
    client = ClientFactory(telegram_id=123456789)
    mock_telebot_class = mocker.MagicMock()
    mock_instance = mocker.MagicMock()
    
    mock_telebot_class.return_value = mock_instance
    mock_instance.send_message.side_effect = TelegramNotificationFailedException
    
    monkeypatch.setattr(views, "TeleBot", mock_telebot_class)
    
    
    resp = api_client.post(
        "/notifications/send-telegram-message", 
        data={"client_id": client.pk, "text": "hello"}
    )
    
    assert resp.status_code == 503

@pytest.mark.django_db
def test_400_if_client_has_no_email(api_client):
    client = ClientFactory()

    client.email = None
    client.save()

    resp = api_client.post("/notifications/send-email", data={"client_id": client.pk, "text": "test"})
    assert resp.status_code == 400

@pytest.mark.django_db
def test_503_if_email_is_not_sent(api_client, mocker, monkeypatch):
    client = ClientFactory()
    send_email = mocker.MagicMock()
    send_email.side_effect = EmailNotificationFailedException

    monkeypatch.setattr(views, "send_mail", send_email)

    resp = api_client.post("/notifications/send-email", data={"client_id": client.pk, "text": "test"})
    assert resp.status_code == 503

@pytest.mark.django_db
def test_method_switching(api_client, mocker, monkeypatch):
    client = ClientFactory()
    mock_telebot_class = mocker.MagicMock()
    mock_instance = mocker.MagicMock()
    
    mock_telebot_class.return_value = mock_instance

    send_sms = mocker.MagicMock()
    send_email = mocker.MagicMock()
    
    monkeypatch.setattr(views, "TeleBot", mock_telebot_class)
    monkeypatch.setattr(views, "send_mail", send_email)
    monkeypatch.setattr(views, "send_sms", send_sms)

    resp = api_client.post("/notifications/send-all", data={"client_id": client.pk, "text": "hello"})
    data = json.loads(resp.text)
    assert resp.status_code == 200
    assert list(data.values()) == [True, True, True]

    client.phone = None
    client.save()

    send_sms.side_effect = SmsNotificationFailedException

    resp = api_client.post("/notifications/send-all", data={"client_id": client.pk, "text": "hello"})
    data_no_phone = json.loads(resp.text)
    assert resp.status_code == 200
    assert list(data_no_phone.values()) == [True, True, False]

    client.email = None
    client.save()

    send_email.side_effect = EmailNotificationFailedException

    resp = api_client.post("/notifications/send-all", data={"client_id": client.pk, "text": "hello"})
    data = json.loads(resp.text)
    assert resp.status_code == 200
    assert list(data.values()) == [True, False, False]