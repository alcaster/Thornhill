from django.db import models


class Message(models.Model):
    from_email = models.CharField(max_length=128)
    to_email = models.CharField(max_length=128)
    subject = models.CharField(max_length=128)
    message = models.TextField(blank=True)
    scheduled = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now=True)
    attachment = models.FileField(upload_to='attachments', blank=True)
    send = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.subject
