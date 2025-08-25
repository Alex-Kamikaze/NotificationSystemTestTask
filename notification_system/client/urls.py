from django.urls import path
from .views import NotificationApiView, SendSmsNotificationView, SendEmailNotificationView, SendTelegramNotificationView

urlpatterns = [
    path("send-all", NotificationApiView.as_view()),
    path("send-email", SendEmailNotificationView.as_view()),
    path("send-telegram-message", SendTelegramNotificationView.as_view()),
    path("send-sms", SendSmsNotificationView.as_view())
]