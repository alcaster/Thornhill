from rest_framework import serializers

from thornhillsystem.models import Message


class EmailsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Message
        fields = ('from_email', 'to_email', 'subject', 'message', 'scheduled', 'creation_date', 'attachment', 'sent')
