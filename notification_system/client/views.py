from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from sms import send_sms
from django.core.mail import send_mail
from telebot import TeleBot
from django.conf import settings
from .serializers import SendNotificationRequestSerializer, NotificationResultsSerializer
from .models import Client
from .mediator_service import MediatorService
from .exceptions import NoNotificationMethodException


class NotificationApiView(APIView):
    
    def post(self, request: Request):
        request_data = SendNotificationRequestSerializer(data=request.data)
        request_data.is_valid(raise_exception=True)
        client = None
        results = None

        try:
            client = Client.objects.get(pk=request_data.validated_data.get("client_id"))
        except Client.DoesNotExist:
            return Response(data=f"Клиента с id {request.validated_data.get('client_id')} не существует!", status=status.HTTP_404_NOT_FOUND)

        bot = TeleBot(token=settings.TELEGRAM_BOT_TOKEN)
        service = MediatorService(send_sms=send_sms, send_email=send_mail, telegram_bot=bot, client=client)
        try:
            results = service.send_all_notifications(request_data.validated_data.get("text"))
        except NoNotificationMethodException:
            return Response(data="У клиента не указаны способы отправки уведомлений", status=status.HTTP_400_BAD_REQUEST)
        else:
            response_data = NotificationResultsSerializer(data=results.__dict__)
            response_data.is_valid()
            if not any([results.email, results.sms, results.telegram]):
                return Response(data="Не удалось отправить уведомления", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(data=response_data.validated_data, status=status.HTTP_200_OK)