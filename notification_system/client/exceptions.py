class NoEmailException(Exception):
    pass

class EmailNotificationFailedException(Exception):
    pass

class NoPhoneException(Exception):
    pass

class SmsNotificationFailedException(Exception):
    pass

class NoTelegramException(Exception):
    pass

class TelegramNotificationFailedException(Exception):
    pass

class NoNotificationMethodException(Exception):
    pass