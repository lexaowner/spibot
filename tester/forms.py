import django_filters
from django import forms
from django.contrib.auth.forms import UserCreationForm as _UserCreationForm, UserChangeForm as _UserChangeForm
from django.core.exceptions import ValidationError
from .models import *


class TicketForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)  # populates the post
        self.fields['master'].queryset = User.objects.filter(groups__name='Мастер')
        self.fields['operator'].queryset = User.objects.filter(groups__name='Опер')

    def clean(self):
        cleaned_data = super().clean()
        district = cleaned_data.get('district')
        street = cleaned_data.get('street')
        apartment = cleaned_data.get('apartment')
        house = cleaned_data.get('house')

        # Проверка наличия дубликата объекта Ticket в базе данных
        existing_tickets = Ticket.objects.filter(
            district=district.id,
            street=street.id,
            house=house,
            apartment=apartment,
            deleted=False,
            # Добавьте другие поля, если они должны быть уникальными
        )

        if self.instance:
            # Если это редактирование, исключите текущий объект из поиска дубликатов
            existing_tickets = existing_tickets.exclude(pk=self.instance.pk)

        if existing_tickets.exists():
            # Добавьте ошибку для конкретного поля, но оставьте значение в поле
            self.add_error('district', 'Такой объект Ticket уже существует.')
            self.add_error('street', 'Такой объект Ticket уже существует.')
            self.add_error('house', 'Такой объект Ticket уже существует.')
            self.add_error('apartment', f"Такой объект Ticket уже существует. /edit_ticket/{existing_tickets.first().id}")

        return cleaned_data

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
    def __init__(self, data=None, user=None, *args, **kwargs):
        if user and user.has_perm('tester.master'):
            if data is not None:
                data = data.copy()
                data.setdefault("status", None)
        else:
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

    status = django_filters.ChoiceFilter(choices=[(True, 'Открыта'), (False, 'Закрыта')], label="Статус",)

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


class ShutdownFilter(django_filters.FilterSet):
    master = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(groups__name='Мастер'),
        label="Мастер",
        widget=forms.Select(attrs={'class': 'master'}),
    )

    class Meta:
        model = Shutdown
        fields = [
            "street",
            "house",
            "apartment",
            "master"
        ]


class ShutdownFilterMaster(django_filters.FilterSet):
    class Meta:
        model = Shutdown
        fields = [
            "street",
            "house",
            "apartment",
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
    telegram_id = forms.CharField(max_length=10, required=False, label=('Telegram ID'))
    class Meta:
        model = User
        fields = ('username', 'email', 'telegram_id',)


class UserChangeForm(_UserChangeForm):
    telegram_id = forms.CharField(max_length=10, required=False, label=('Telegram ID'))
    class Meta:
        model = User
        fields = ('username', 'email', 'telegram_id',)


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


class Shutdownlist(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Shutdownlist, self).__init__(*args, **kwargs)
        self.fields['completion'].label = ''

    class Meta:
        model = Shutdown
        fields = [
            'completion',
            ]
        widgets = {
            'completion': forms.CheckboxInput(attrs={'class': 'checkbox-class'}),
        }


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
