from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

def start_page(request):

    if request.user.is_authenticated:
        obj = Ticket.objects.all()
        context = {
            "obj": obj,
        }
        return render(request, 'tester/start_page.html', context)

    else:

        return render(request,'tester/login_form.html')


def add_ticket(request):

    if request.user.is_authenticated:
        if request.method  == 'POST':
            forms = Addticket(request.POST)
            forms.save()
            return redirect('start_page')

        form = Addticket()
        context = {
            "forms": form,
        }

        return render(request, 'tester/add_ticket.html', context)

def login_cora_2(request):
    if request.user.is_authenticated:
        redirect('start_page')

    elif request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            login(request, user)
            return redirect('start_page')
        else:
            redirect('')

    else:
        redirect('start_page')





