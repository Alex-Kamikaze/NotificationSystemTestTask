from django.contrib import admin
from .models import Client

# Register your models here.
@admin.register(Client)
class ClientAdminModel(admin.ModelAdmin):
    search_fields=["fio", "telegram_id", "email", "phone"]