from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect

from Thornhill.settings.base import BASE_DIR
from thornhillsystem.forms import MessageForm
from thornhillsystem.models import Message, Temperature
from thornhillsystem.temperature_system.temperature import get_temp
from .tasks import send_email_task


def index(request):
    context_dict = []
    return render(request, 'thornhillsystem/index.html', context=context_dict)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'thornhillsystem/login.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def email_sender(request):
    messages = Message.objects.order_by('creation_date')
    form = MessageForm()
    context_dict = {'messages': messages, 'form': form}
    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            message = form.save(commit=False)
            path = None
            if message.attachment:
                print(BASE_DIR)
                print(message.attachment.url)
                path = BASE_DIR + message.attachment.url

            if form.cleaned_data['send_now']:
                message.task_id = send_email_task.delay(
                    message.from_email, message.to_email, message.subject, message.message, path)
                message.sent = True
            else:
                when = message.scheduled
                message.task_id = send_email_task.apply_async(
                    (message.from_email, message.to_email, message.subject, message.message, path),
                    eta=when)
            message.save()
            return redirect('email_sender')
        else:
            print(form.errors)
    else:
        return render(request, 'thornhillsystem/email_sender.html', context_dict)


@login_required()
def temperature(request):
    context_dict = {}
    last_temperature = get_temp()
    temperatures = Temperature.objects.order_by('-timestamp')[:30]
    context_dict['last_temperature'] = last_temperature
    context_dict['temperatures'] = temperatures
    return render(request, 'thornhillsystem/temperature.html', context=context_dict)
