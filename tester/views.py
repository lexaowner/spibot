from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import time


def start_page(request):
    if request.user.is_authenticated:
        obj = Ticket.objects.all()
        username = request.user.get_username()
        is_super = bool(request.user.is_superuser)
        context = {
            "obj": obj,
            "username": username,
            "is_super": is_super,
        }
        return render(request, 'tester/start_page.html', context)

    else:

        return redirect("login")


@login_required(login_url='login')
def add_ticket(request):
    username = request.user.get_username()
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = Addticket(request.POST)
            form.changed_data['operator'] = request.user.id


            form.save()
            return redirect('start_page')

    form = Addticket()
    context = {
        "form": form,
        "username": username
    }
    return render(request, 'tester/add_ticket.html', context)


def login_cora_2(request):
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            messages.success(request, 'Вы вошли в систему')
            login(request, user)
            return redirect('start_page')

    else:
        messages.error(request, 'Имя или логин введеный не верно')
        redirect('login')

    return render(request, 'tester/login_form.html')


def logout_cora_2(request):
    logout(request)
    return redirect('start_page')


def profile(request):
    person = Person.objects.get(pk=request.user.id)
    username = request.user.get_username()
    user = User.objects.get(pk=request.user.id)
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')
    if password:
        if password == password_confirm:
            user.set_password(password)
            messages.success(request, 'Пароль обновлен')
        else:
            messages.error(request, 'Пароли не совпадают, текущий пароль не изменен')
    user.save()
    context = {
        "user": user,
        "username": username,
        "person": person
    }
    return render(request, 'tester/profile.html', context)


def EditTicketForm(request, id):
    if request.method == 'POST':
        forms = Addticket(request.POST)
        forms.save()
        return redirect('start_page')

    username = request.user.get_username()
    form = Ticket.objects.get(id=id)
    edit_from = Addticket(request.POST, instance=form)
    context = {
        "e_form": edit_from,
        "username": username
    }

    return render(request, 'tester/edit_ticketfrom.html', context)
