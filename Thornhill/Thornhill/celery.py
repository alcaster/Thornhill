import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

from thornhillsystem.temperature_system import temperature

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "Thornhill.settings.base")

app = Celery('Thornhill')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='0,30'), update_temp.s(), name='update_temp')


@app.task
def update_temp():
    from thornhillsystem.models import Temperature
    temp = Temperature(temperature=temperature.get_temp())
    temp.save()
    temperature.rebuild_chart()
