from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
import time


def start_page(request):
    if request.user.is_authenticated:
        # get_user = User.objects.get(id=request.user.id)
        # if get_user.has_perm("tester.master"):
        #     if request.method == "POST":
        #         form_add_com_master = AddComMaster(request.POST)
        #         form_add_com_master.save()
        #         return redirect('start_page')

        # if request.method == 'PUT':
        #     mst_id = Addticket.objects.get(master=request.POST)
        #     mst_id.save()

        get_mater_ticket = Ticket.objects.filter(master=request.user.id)
        master_aad_com = AddComMaster
        # messages.error(request, f'{get_user.has_perm("tester.operator")}')
        change_master = Addticket()
        obj = Ticket.objects.all()
        username = request.user.get_username()
        is_super = bool(request.user.is_superuser)
        context = {
            "obj": obj,
            "username": username,
            "is_super": is_super,
            "master_ticket": get_mater_ticket,
            "mas_com": master_aad_com,
            "change_master": change_master,
        }
        return render(request, 'tester/start_page.html', context)

    else:
        return redirect("login")


@permission_required('tester.operator', login_url='error')
def add_ticket(request):
    username = request.user.get_username()
    if request.user.is_authenticated:
        if request.method == 'POST':
            handle_edit(request)
            return redirect('start_page')

    form = Addticket()
    context = {
        "form": form,
        "username": username
    }
    return render(request, 'tester/add_ticket.html', context)


def handle_edit(request, instance=None):
    form = Addticket(request.POST, instance=instance)
    if form.is_valid():
        messages.success(request, f'{instance} данные успешно изменены ')
        form.save()
    else:
        messages.error(request,f'Данные не могут быть изменены {Exception()}')


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
    return redirect('login')


def profile(request):
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
    }
    return render(request, 'tester/profile.html', context)


def edit_ticket(request, pk):
    if request.method == 'POST':
        try:
            instance = Ticket.objects.get(id=pk)
            handle_edit(request, instance)
            return redirect('edit_ticket', pk)
        except:
            messages.error(request, f'{Exception()}')
    username = request.user.get_username()
    on = Ticket.objects.get(id=pk)
    edit_from = TicketEditForm(instance=on)
    context = {
        "e_form": edit_from,
        "username": username
    }

    return render(request, 'tester/edit_ticketfrom.html', context)


def error(request):
    messages.error(request, 'Недостаточно прав')
    return render(request, 'tester/error.html')

def log(request, pk):
    username = request.user.get_username()
    get_odj = Ticket.objects.get(id=pk)
    history = get_odj.history.all()
    context = {
        "history": history,
        "username": username,
    }
    return render(request, 'tester/log.html', context)

def test(request):
    return render(request, 'tester/test.html')
