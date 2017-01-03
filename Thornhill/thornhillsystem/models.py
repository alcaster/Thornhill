from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Message(models.Model):
    from_email = models.CharField(max_length=128)
    to_email = models.CharField(max_length=128)
    subject = models.CharField(max_length=128)
    message = models.TextField(blank=True)
    scheduled = models.DateTimeField()
    creation_date = models.DateTimeField(auto_now=True)
    attachment = models.FileField(upload_to='attachments', blank=True)

    sent = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Messages'

    def __str__(self):
        return self.subject
