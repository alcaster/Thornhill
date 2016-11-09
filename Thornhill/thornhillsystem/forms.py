from django import forms
from thornhillsystem.models import Message
from django.forms.widgets import TextInput
import datetime


class MessageForm(forms.ModelForm):
    from_email = forms.CharField(max_length=128, help_text="From which email.")
    to_email = forms.CharField(max_length=128, help_text="To whom")
    subject = forms.CharField(max_length=128, help_text="Subject")
    message = forms.CharField(blank=True, widget=TextInput, required=False)
    scheduled = forms.DateTimeField(initial=datetime.date.today, help_text="Date and time to be sent")
    creation_date = forms.DateTimeField(widget=forms.HiddenInput(), initial=datetime.date.today)
    attachment = forms.FileField(required=False)
    send = forms.BooleanField(widget=forms.HiddenInput())

    class Meta:
        model = Message
        fields = ('from_email', 'to_email', 'subject', 'message', 'scheduled', 'attachment')
