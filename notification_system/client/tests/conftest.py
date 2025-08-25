import pytest
from rest_framework.test import APIClient
from ..mediator_service import MediatorService

@pytest.fixture
def send_notification(mocker):
    return mocker.MagicMock()

@pytest.fixture
def telebot(mocker):

    bot = mocker.MagicMock()
    bot.send_message = mocker.MagicMock()
    return bot

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def mock_mediator_service(send_notification, telebot):
    return MediatorService(send_sms=send_notification, send_email=send_notification, telegram_bot=telebot, client=None)