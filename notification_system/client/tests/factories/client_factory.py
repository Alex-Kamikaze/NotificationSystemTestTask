import factory
from ...models import Client

class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    fio = "Тест Тест Тест"
    telegram_id = 1
    phone = "+7900000000"
    email = "test@test.ru"