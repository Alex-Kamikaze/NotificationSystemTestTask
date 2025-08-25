# Система оповещений
Система оповещений по email, sms и Telegram. 

## Документация по API
(Мне лень было Swagger делать :p)
* ``` POST /notifications/send-all ``` - Отправляет уведомления по всем каналам
* ``` POST /notifications/send-sms ``` - Отправляет уведомление по СМС
* ``` POST /notifications/send-email ``` - Отправляет управление по Email
* ``` POST /notifications/send-telegram-message ``` - Отправляет уведомление ввиде сообщения от бота в Telegram

## Настройка окружения
Конфиг .env:
``` 
SECRET_KEY="SECRET_KEY"
DEBUG=True
ALLOWED_HOSTS=*

EMAIL_HOST=''
EMAIL_PORT=999
EMAIL_USE_TLS=False
EMAIL_USE_SSL=True
EMAIL_HOST_USER='sample@mail.ru'
EMAIL_HOST_PASSWORD='...'
DEFAULT_FROM_EMAIL="sample@mail.ru"

SMS_BACKEND = 'sms.backends.console.SmsBackend'
SMS_FILE_PATH = '/tmp/messages'
SMS_SENDER="..."
```

## Запуск проекта
```
uv sync
uv run python manage.py migrate
uv run python manage.py runserver
```
