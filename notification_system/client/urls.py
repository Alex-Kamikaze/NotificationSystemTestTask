from django.urls import path
from .views import NotificationApiView

urlpatterns = [
    path("send", NotificationApiView.as_view())
]