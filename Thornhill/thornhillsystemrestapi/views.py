from datetime import datetime

from celery.task.control import revoke
from rest_framework import status
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from Thornhill.settings.base import BASE_DIR
from thornhillsystem.models import Message
from thornhillsystem.tasks import send_email_task
from thornhillsystemrestapi.serializers import EmailsSerializer


class MailViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Message.objects.all()
    serializer_class = EmailsSerializer

    def create(self, request, **kwargs):
        print("Custom creation")
        serializer = EmailsSerializer(data=request.data)
        if serializer.is_valid():
            content = serializer.data
            send_now = content['send_now']
            del content['send_now']
            message = Message(**content)
            path = None
            if message.attachment:
                path = BASE_DIR + message.attachment.url
            if send_now:
                message.task_id = send_email_task.delay(
                    message.from_email, message.to_email, message.subject, message.message, path)
                message.sent = True
            else:
                when = message.scheduled
                print(when)
                when = datetime.strptime(when,
                                         '%Y-%m-%dT%H:%M:%S%z:00')  # problem with time parsing (timezone end +01:00)
                message.task_id = send_email_task.apply_async(
                    (message.from_email, message.to_email, message.subject, message.message, path),
                    eta=when)
            message.save()
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        message = Message.objects.get(pk=pk)
        if not message.sent:
            revoke(task_id=message.task_id, terminate=True)
        message.delete()
        return Response(status=status.HTTP_400_BAD_REQUEST)
