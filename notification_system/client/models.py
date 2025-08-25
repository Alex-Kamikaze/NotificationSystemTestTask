from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class Client(models.Model):
    """ Пользователь системы, которому может быть отправлено уведомление """

    fio = models.CharField(max_length=1024, verbose_name="ФИО Клиента")
    telegram_id = models.IntegerField(verbose_name="ID в телеграмме", unique=True, null=True, blank=True)
    email = models.EmailField(verbose_name="Электронная почта", null=True, blank=True)
    phone = PhoneNumberField(blank=True, verbose_name="Номер телефона", null=True)

    def __str__(self):
        return self.fio
    
    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"
        ordering=["fio"]