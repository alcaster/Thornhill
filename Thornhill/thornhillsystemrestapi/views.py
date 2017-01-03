from rest_framework import viewsets, permissions

from thornhillsystem.models import Message
from thornhillsystemrestapi.serializers import EmailsSerializer


class MailViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Message.objects.all()
    serializer_class = EmailsSerializer
