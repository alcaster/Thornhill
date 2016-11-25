from Thornhill.celery import app
from thornhillsystem.email_system.email_sender import Sender
from thornhillsystem.models import Message


@app.task
def test(param):
    return 'The test task executed with argument "%s" ' % param


@app.task
def send_email_task(from_email, to_mail, subject, message, attachment_path=None):
    sender = Sender(from_email)
    sender.send_message(to_mail, subject, message, attachment_path)
    mes_obj = Message.objects.get(from_email=from_email, to_email=to_mail, subject=subject, message=message)
    mes_obj.sent = True
    mes_obj.save()
