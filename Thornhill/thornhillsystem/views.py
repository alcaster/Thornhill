from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from thornhillsystem.models import Message


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


@login_required()
def email_sender(request):
    if request.method == 'POST':
        pass
    else:
        messages = Message.objects.order_by('creation_date')
        context_dict = {'messages': messages}
        return render(request, 'thornhillsystem/email_sender.html', context_dict)
