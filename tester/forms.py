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
            "cause",
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
    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            data.setdefault("status", True)
        super(TicketFilterForm, self).__init__(data, *args, **kwargs)

    master = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(groups__name='Мастер'),
        label="Мастер",
        widget=forms.Select(attrs={'class': 'master'}),
    )

    operator = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(groups__name='Опер'),
        label="Оператор",
        widget=forms.Select(attrs={'class': 'operator'}),
    )

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


class TicketFilterFormProcessing(django_filters.FilterSet):
    master = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(groups__name='Мастер'),
        label="Мастер",
        widget=forms.Select(attrs={'class': 'master'}),
    )

    operator = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(groups__name='Опер'),
        label="Оператор",
        widget=forms.Select(attrs={'class': 'operator'}),
    )

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
        ]


class AddComMaster(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'comment_master',
            'cause',
            'status',
        ]


class UserCreationForm(_UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserChangeForm(_UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class ShutdownForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ShutdownForm, self).__init__(*args, **kwargs)  # populates the post
        self.fields['master'].queryset = User.objects.filter(groups__name='Мастер')

    class Meta:
        model = Shutdown
        fields = [
            'file',
            'master'
        ]


class AddDistrict(forms.ModelForm):
    class Meta:
        model = District
        fields = [
            'region',
            'name'
        ]


class AddStreet(forms.ModelForm):
    class Meta:
        model = Street
        fields = [
            'district',
            'name'
        ]
