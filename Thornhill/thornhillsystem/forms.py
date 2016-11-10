from django import forms
from thornhillsystem.models import Message
from django.forms.widgets import TextInput
import datetime


class MessageForm(forms.ModelForm):
    from_email = forms.EmailField(max_length=128, help_text="From email")
    to_email = forms.EmailField(max_length=128, help_text="To whom")
    subject = forms.CharField(max_length=128, help_text="Subject")
    message = forms.CharField(required=False, widget=TextInput, help_text="Message")
    scheduled = forms.DateTimeField(initial=datetime.date.today, help_text="Date and time to be sent")
    attachment = forms.FileField(required=False, help_text="Attachment")
    sent_now = forms.BooleanField(required=False, help_text="Sent now ?")

    class Meta:
        model = Message
        fields = ('from_email', 'to_email', 'subject', 'message', 'scheduled',
                  'attachment')
