from rest_framework import serializers

from thornhillsystem.models import Message


class EmailsSerializer(serializers.HyperlinkedModelSerializer):
    send_now = serializers.BooleanField(required=False, help_text="Send now ?")

    class Meta:
        model = Message
        fields = ('url', 'id',
                  'from_email', 'to_email', 'subject', 'message', 'scheduled', 'creation_date', 'attachment',
                  'send_now')
