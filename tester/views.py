from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
import time


def ticket_filter_form(request, filters={}):
    fields = [
        'district',
        'street',
        'house',
        'apartment',
        'date',
        'closed_date',
        'completion_date',
        'login',
        'first_contact',
        'second_contact',
        'comment_master',
        'comment_operator',
        'update',
        'operator',
        'master',
        'status',
    ]

    for k, v in request.GET.items():
        if len(v) and k in fields:
            if k == 'status':
                v = v == 'True'
            if k == 'district':
                k = 'district_id'
                v = int(v)
            if k == 'street':
                k = 'street_id'
                v = int(v)

            filters.update({k: v})
            print(filters)
    return Ticket.objects.filter(**filters), TicketFilterForm(request.GET,initial=filters)


def start_page(request):
    if request.user.is_authenticated:

        if request.method == 'GET':
            redirect('start_page')
        get_mater_ticket = Ticket.objects.filter(master=request.user.id)
        # messages.error(request, f'{get_user.has_perm("tester.operator")}')
        change_master = TicketForm()

        tickets, filter_form = ticket_filter_form(request, )
        username = request.user.get_username()
        is_super = bool(request.user.is_superuser)
        context = {
            "tickets": tickets,
            "username": username,
            "is_super": is_super,
            "master_ticket": get_mater_ticket,
            "change_master": change_master,
            "filter_form": filter_form
        }
        return render(request, 'tester/start_page.html', context)

    else:
        return redirect("login")


def add_com_master(request, pk):
    if request.method == 'POST':
        try:
            instance = Ticket.objects.get(id=pk)
            com_master_edit(request, instance)
            return redirect('start_page')
        except:
            messages.error(request, f'Данные не могут быть изменены {Exception()}')

    username = request.user.get_username()
    on = Ticket.objects.get(id=pk)
    edit_from = AddComMaster(instance=on)
    context = {
        "username": username,
        "form": edit_from,
    }
    return render(request, 'tester/add_comment_master.html', context)


@permission_required('tester.operator', login_url='error')
def add_ticket(request):
    username = request.user.get_username()
    if request.user.is_authenticated:
        if request.method == 'POST':
            handle_edit(request)
            return redirect('start_page')

    form = TicketForm()
    context = {
        "form": form,
        "username": username
    }
    return render(request, 'tester/add_ticket.html', context)


def com_master_edit(request, instance=None):
    form = AddComMaster(request.POST, instance=instance)
    if form.is_valid():
        ticket = form.save(commit=False)
        ticket.save()
        messages.success(request,
                         f'Добавлен коментарий к заявке {instance.street}  {instance.house} кв {instance.apartment}')
    else:
        messages.error(request, f'Данные не могут быть изменены {Exception(request)}')


def handle_edit(request, instance=None):
    form = TicketForm(request.POST, instance=instance)
    if form.is_valid():
        ticket = form.save(commit=False)
        ticket.operator = request.user
        ticket.save()
    else:
        messages.error(request, f'Данные не могут быть изменены {Exception(request)}')


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
            messages.success(request,
                             f'Данные успешно изменены {instance.street}  {instance.house} кв {instance.apartment}')
            return redirect('edit_ticket', pk)
        except:
            messages.error(request, f'Данные не могут быть изменены {Exception()}')
    username = request.user.get_username()
    on = Ticket.objects.get(id=pk)
    edit_from = TicketForm(instance=on)
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
    # history_old = history.prev_record
    # messages.error(request, f'{history_old}')

    context = {
        "history": history,
        "username": username,
    }
    return render(request, 'tester/log.html', context)


def test(request):
    get_mater_ticket = Ticket.objects.filter(master=request.user.id)
    # messages.error(request, f'{get_user.has_perm("tester.operator")}')
    change_master = TicketForm()
    username = request.user.get_username()
    is_super = bool(request.user.is_superuser)
    context = {
        "username": username,
        "is_super": is_super,
        "master_ticket": get_mater_ticket,
        "change_master": change_master,
    }
    return render(request, 'tester/test.html', context)
