from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from thornhillsystem.models import Message
from thornhillsystem.forms import MessageForm
from thornhillsystem.email_system.email_sender import Sender


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
            if form.cleaned_data['sent_now']:
                sender = Sender(message.from_email)
                sender.send_message(message.to_email, message.subject, message.message)
                message.send = True

            message.save()
            return redirect('email_sender')
        else:
            print(form.errors)
    else:
        return render(request, 'thornhillsystem/email_sender.html', context_dict)
