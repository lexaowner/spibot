import django_filters
from django import forms
from django.contrib.auth.forms import UserCreationForm as _UserCreationForm, UserChangeForm as _UserChangeForm

from .models import *


class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)  # populates the post
        self.fields['master'].queryset = User.objects.filter(groups__name='Мастер')
        self.fields['operator'].queryset = User.objects.filter(groups__name='Опер')

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
            "type",
            "master",
            "priority",
            "comment_operator",
            "comment_master",
            "operator",
            "status"
        ]


class NewsForm(forms.ModelForm):

    class Meta:
        model = News
        fields = [
            "title",
            "text",
        ]


class TicketFilterForm(django_filters.FilterSet):

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
            "type",
            "operator",
            "master",
            "priority",
            "status",
        ]


class AddComMaster(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'comment_master',
            'status'
        ]


class UserCreationForm(_UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserChangeForm(_UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')
