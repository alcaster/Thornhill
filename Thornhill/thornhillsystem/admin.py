from django.contrib import admin

from thornhillsystem.models import Message, Temperature


class MessageAdmin(admin.ModelAdmin):
    list_display = ('from_email', 'to_email', 'subject',
                    'message', 'scheduled', 'creation_date', 'attachment', 'sent')


class TemperatureAdmin(admin.ModelAdmin):
    list_display = ('temperature', 'timestamp')


admin.site.register(Message, MessageAdmin)
admin.site.register(Temperature, TemperatureAdmin)
