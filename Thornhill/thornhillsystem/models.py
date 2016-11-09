from django.db import models


class Message(models.Model):
    from_email = models.CharField(max_length=128, unique=True)
    to_email = models.CharField(max_length=128)
    subject = models.CharField(max_length=128)
    message = models.TextField()
    scheduled = models.DateTimeField(blank=True)
    creation_date = models.DateTimeField(auto_now=True)
