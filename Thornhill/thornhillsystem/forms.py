from django import forms
from thornhillsystem.models import Message
from django.forms.widgets import TextInput
import datetime
from thornhillsystem.email_system.email_sender import get_all_accounts


def get_choices_from_list(filename):
    return [(i, i) for i in get_all_accounts(filename)]


class MessageForm(forms.ModelForm):
    subject = forms.CharField(max_length=128, help_text="Subject")
    message = forms.CharField(required=False, widget=TextInput, help_text="Message")
    scheduled = forms.DateTimeField(initial=datetime.datetime.now(), help_text="Date and time to be sent")
    attachment = forms.FileField(required=False, help_text="Attachment")
    send_now = forms.BooleanField(required=False, help_text="Send now ?")

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['from_email'] = forms.ChoiceField(
            choices=get_choices_from_list('accounts.json'), help_text="From ")
        self.fields['to_email'] = forms.ChoiceField(
            choices=get_choices_from_list('receivers.json'), help_text="To whom ")

    class Meta:
        model = Message
        fields = ('from_email', 'to_email', 'subject', 'message', 'attachment', 'send_now', 'scheduled')
