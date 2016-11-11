from django.contrib import admin
from thornhillsystem.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('from_email', 'to_email', 'subject',
                    'message', 'scheduled', 'creation_date', 'attachment', 'sent')


admin.site.register(Message, MessageAdmin)
