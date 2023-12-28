import os
import time
import pandas as pd
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from reversion.models import Version



def start_page(request):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            proc = Ticket.objects.get_queryset_none().filter(viewed=False).values('id', 'district', 'street', 'house',
                                                                                  'apartment',
                                                                                  'date', 'date_change', 'closed_date',
                                                                                  'completion_date', 'login',
                                                                                  'first_contact',
                                                                                  'second_contact', 'comment_master',
                                                                                  'comment_operator', 'operator__id',
                                                                                  'operator__username', 'master__id',
                                                                                  'master__username', 'type',
                                                                                  'priority', 'status',
                                                                                  'cause', 'user_change', 'viewed',
                                                                                  'deleted')
            user_per = list(request.user.get_group_permissions())

            data = {'tickets': list(proc), 'user_permissions': user_per}
            return JsonResponse(data, safe=False)

        if request.method == 'POST':
            form = NewsForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,
                                 f'Новость добавлена')
                redirect('start_page')
            else:
                messages.error(request, f'Новость не может быть добавлена {Exception(request)}')

            return redirect('start_page')

        elif request.method == 'GET':
            username = request.user.get_username()
            ticket_time = timezone.now()
            is_super = bool(request.user.is_superuser)
            get_mater_ticket = TicketFilterForm(request.GET,
                                                queryset=Ticket.objects.get_master(id=request.user.id).order_by(
                                                    "-date"))
            news = News.objects.order_by("-date")
            news_form = NewsForm()
            change_master = TicketForm()
            tickets = TicketFilterForm(request.GET, queryset=Ticket.objects.get_queryset_true())
            paginator = Paginator(tickets.qs, 37)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)

            context = {
                "tickets": tickets,
                "page_obj": page_obj,
                "username": username,
                "is_super": is_super,
                "master_ticket": get_mater_ticket,
                "change_master": change_master,
                "news": news,
                "n_form": news_form,
                "time": ticket_time,
                "pages": paginator.page_range,

            }

            return render(request, 'tester/start_page.html', context)

    else:
        return redirect("login")


@permission_required('tester.master', login_url='error')
def add_com_master(request, pk):
    if request.method == 'POST':
        try:
            instance = Ticket.objects.get(id=pk)
            com_master_edit(request, instance)

        except:
            messages.error(request, f'Данные не могут быть изменены {Exception()}')

    username = request.user.get_username()
    year_now = timezone.now()
    on = Ticket.objects.get(id=pk)
    edit_from = AddComMaster(instance=on)
    context = {
        "username": username,
        "form": edit_from,
        "year_now": year_now
    }
    return render(request, 'tester/add_comment_master.html', context)


@permission_required('tester.operator', login_url='error')
def add_ticket(request):
    news = News.objects.all()
    ticket_time = timezone.now()
    username = request.user.get_username()
    year_now = timezone.now()
    proc = Ticket.objects.get_queryset_none()

    if request.user.is_authenticated:
        if request.method == 'POST':
            instance = None
            form = TicketForm(request.POST, instance=instance)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.operator = request.user
                ticket.status = None
                ticket.comment_master = None
                ticket.user_change = request.user.first_name
                ticket.save()
                if ticket.id:
                    return redirect('edit_ticket', ticket.id)

            else:
                messages.error(request, "Такой объект Ticket уже существует")


    form = TicketForm()
    context = {
        "form": form,
        "username": username,
        "year_now": year_now,
        "news": news,
        "time": ticket_time,
        "processing": proc,
    }
    return render(request, 'tester/add_ticket.html', context)


@permission_required('tester.master', login_url='error')
def com_master_edit(request, instance=None):
    form = AddComMaster(request.POST, instance=instance)
    if form.is_valid():
        ticket = form.save(commit=False)
        ticket.user_change = request.user.get_username()
        ticket.save()

        if instance.apartment is None:
            messages.success(request,
                             f'Данные успешно изменены {instance.street}  {instance.house}')

        else:
            messages.success(request,
                             f'Данные успешно изменены {instance.street}  {instance.house} кв {instance.apartment}')

        return redirect('master_comment', ticket.id)

    else:
        messages.error(request, f'Данные не могут быть изменены {Exception(request)}')


def login_cora_2(request):
    year_now = timezone.now()
    context = {
        "year_now": year_now
    }
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            messages.success(request, 'Вы вошли в систему')
            login(request, user)
            return redirect('start_page')

        else:
            messages.error(request, 'Логин или пароль введеный не верно')
            redirect('login')

    return render(request, 'tester/login_form.html', context=context)


def logout_cora_2(request):
    logout(request)
    return redirect('login')


def profile(request):
    username = request.user.get_username()
    year_now = timezone.now()
    user = User.objects.get(pk=request.user.id)
    password = request.POST.get('password')
    password_confirm = request.POST.get('password_confirm')
    first_name = request.POST.get('first_name')

    if first_name:
        user.first_name = first_name
        user.save()

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
        "time": year_now
    }
    return render(request, 'tester/profile.html', context)


@permission_required('tester.dispatcher', login_url='error')
def processing(request):
    if request.user.is_authenticated:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            proc = Ticket.objects.get_queryset_none().filter(viewed=False).values('id', 'district', 'street', 'house',
                                                                                  'apartment',
                                                                                  'date', 'date_change', 'closed_date',
                                                                                  'completion_date', 'login',
                                                                                  'first_contact',
                                                                                  'second_contact', 'comment_master',
                                                                                  'comment_operator', 'operator__id',
                                                                                  'operator__username', 'master__id',
                                                                                  'master__username', 'type',
                                                                                  'priority', 'status',
                                                                                  'cause', 'user_change', 'viewed',
                                                                                  'deleted')
            data = list(proc)
            return JsonResponse(data, safe=False)

    news = News.objects.all()
    ticket_time = timezone.now()
    # messages.error(request, f'{get_user.has_perm("tester.operator")}')
    change_master = TicketForm()
    tickets = TicketFilterFormProcessing(request.GET, queryset=Ticket.objects.get_queryset_none())
    username = request.user.get_username()
    year_now = timezone.now()
    proc = Ticket.objects.filter(status=None)
    is_super = bool(request.user.is_superuser)

    context = {
        "tickets": tickets,
        "username": username,
        "year_now": year_now,
        "is_super": is_super,
        "change_master": change_master,
        "news": news,
        "time": ticket_time,
        "processing": proc,

    }
    return render(request, 'tester/processing.html', context)


@permission_required('tester.operator', login_url='error')
def edit_ticket(request, pk):
    if request.method == "GET":
        if request.user.has_perm("tester.dispatcher"):
            form = Ticket.objects.get(int(pk))
            form.viewed = True
            form.save()
    else:
        pass

    if request.method == 'POST':
        try:
            instance = Ticket.objects.get(id=pk)
            form = TicketForm(request.POST, instance=instance)
            if form.is_valid():
                ticket = form.save(commit=False)
                ticket.viewed = False
                ticket.user_change = request.user.first_name
                ticket.date_change = timezone.now()
                ticket.save()

                if instance.apartment is None:
                    messages.success(request,
                                     f'Данные успешно изменены {instance.street}  {instance.house}')

                else:
                    messages.success(request, f'Данные успешно изменены {instance.street}  {instance.house} кв {instance.apartment}')

                return redirect('edit_ticket', pk)

        except:
            messages.error(request, f'Данные не могут быть изменены {Exception(request)}')

    latest_version = Version.objects.get_for_object(Ticket.objects.get(id=pk))

    messages.success(request, f"{latest_version}")

    get_odj = Ticket.objects.get(id=pk)
    username = request.user.get_username()
    year_now = timezone.now()
    on = Ticket.objects.get(id=pk)
    edit_from = TicketForm(instance=on)
    proc = Ticket.objects.get_queryset_none()

    context = {
        "e_form": edit_from,
        "username": username,
        "year_now": year_now,
        "obj": get_odj,
        "processing": proc,
    }

    return render(request, 'tester/edit_ticketfrom.html', context)


def error(request):
    username = request.user.get_username()
    year_now = timezone.now()
    messages.error(request, 'Недостаточно прав')
    context = {
        "username": username,
        "year_now": year_now,
    }
    return render(request, 'tester/error.html', context)


def log(request):
    username = request.user.get_username()

    context = {
        "username": username,
    }
    return render(request, 'tester/log.html', context)


def handle_uploaded_file(file):
    # Создайте отдельный путь для загруженных файлов
    upload_path = os.path.join(settings.MEDIA_ROOT, 'uploads')
    os.makedirs(upload_path, exist_ok=True)

    # Сохраните файл в новый путь
    fs = FileSystemStorage(location=upload_path)
    filename = fs.save(file.name, file)

    # Загрузите данные Excel с использованием pandas
    excel_path = os.path.join(upload_path, filename)
    df = pd.read_excel(excel_path)

    # Добавьте вашу логику обработки данных здесь

    # Верните данные в представление (здесь просто для примера)
    return render(None, 'tester/shutdown.html', {'data': df.to_html()})


@permission_required('tester.master', login_url='error')
def shutdown(request):
    if request.method == 'POST':
        messages.error(request, request.POST, request.FILES)
        excel_file = request.FILE

        return handle_uploaded_file(excel_file)

    username = request.user.get_username()
    form = ShutdownForm()
    proc = Ticket.objects.get_queryset_none()

    context = {
        "username": username,
        "form": form,
        "processing": proc,
    }
    return render(request, 'tester/shutdown.html', context)


@permission_required('tester.dispatcher', login_url='error')
def add_address(request):
    username = request.user.get_username()
    year_now = timezone.now()
    f = AddStreet()
    d = AddDistrict()
    street = Street.objects.all()
    district = District.objects.all()
    proc = Ticket.objects.get_queryset_none()

    if request.method == "POST":
        form = AddDistrict(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Район добавлен')

    if request.method == "POST":
        form = AddStreet(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Улица добавлена')

    context = {
        "username": username,
        "year_now": year_now,
        "form_street": f,
        "form_district": d,
        "streets": street,
        "districts": district,
        "processing": proc,
    }
    return render(request, 'tester/address.html', context)


def territory(request):
    username = request.user.get_username()
    year_now = timezone.now()
    proc = Ticket.objects.get_queryset_none()
    context = {
        "username": username,
        "year_now": year_now,
        "processing": proc,
    }
    return render(request, 'tester/territory.html', context)


def test(request):
    return render(request, 'tester/test.html')
