from django.shortcuts import render, redirect
from .models import *
from tester.models import Ticket


def start_page(request):
    region = Region.objects.all()
    district = District.objects.all()
    street = Street.objects.all()
    house = House.objects.all()
    ticket = Ticket.objects.all()
    context = {
        "obj": {
        "region": region,
        "district": district,
        "street": street,
        "house": house,
        "ticket": ticket
        }
    }
    return render(request, 'tester/base.html', context)


def add_ticket(request):
    obj = {
        "region": Region,
        "district": District,
        "street": Street,
        "house": House,
        "ticket": Ticket
        }
    return render(request, 'tester/add_ticket.html', obj)
    if request == 'POST':
        pass



