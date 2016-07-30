from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from User.forms import *
from User.models import *


def get_users(request):
    return HttpResponse("Hello User")


def all_users(request):
    if request.method == 'GET':
        form = UserFormMain
        return render(request, 'REST/all_users.html', {'form': form})
    elif request.method == 'POST' and request.is_ajax():
        form = UserFormMain(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = request.POST.get('password')
            user.set_password(password)
            user.save()
            return HttpResponse("Successfully Registered " + request.POST['username'])


def forms(request):
    pass
