from django import forms
from django.forms import Select
from .models import *

class Addticket(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            "district",
            "street",
            "house",
            "apartment",
            "login",
            "first_contact",
            "second_contact",
            "comment_operator",
        ]

