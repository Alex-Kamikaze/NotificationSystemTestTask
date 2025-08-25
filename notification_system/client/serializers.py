from rest_framework import serializers

class SendNotificationRequestSerializer(serializers.Serializer):

    client_id = serializers.IntegerField()
    text = serializers.CharField(max_length = 2048)

class NotificationResultsSerializer(serializers.Serializer):

    telegram = serializers.BooleanField()
    email = serializers.BooleanField()
    sms = serializers.BooleanField()