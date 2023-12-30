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
            # Добавьте другие поля, если они должны быть уникальными
        )

        if self.instance:
            # Если это редактирование, исключите текущий объект из поиска дубликатов
            existing_tickets = existing_tickets.exclude(pk=self.instance.pk)

        if existing_tickets.exists():
            raise ValidationError('Такой объект Ticket уже существует.')

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
    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            data.setdefault("status", True)
        super(TicketFilterForm, self).__init__(data, *args, **kwargs)

        # self.filters['street'] = django_filters.ModelChoiceFilter(
        #     queryset=Street.objects.none(),  # queryset будет установлен в зависимости от выбранного района
        #     label="Улица",
        #     widget=ChainedSelect(
        #         to_app_name='tester',
        #         to_model_name='Ticket',
        #         chained_field='district',
        #         chained_model_field='district',
        #         foreign_key_app_name='tester',
        #         foreign_key_model_name='Street',
        #         foreign_key_field_name='street',
        #         auto_choose=False,
        #         show_all=False,
        #     ),
        # )
        #
        # # Запоминаем выбранный район
        # district = self.data.get('district')
        # if district:
        #     # Обновляем queryset для поля street
        #     self.filters['street'].queryset = Street.objects.filter(district=district)

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

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if not file:
            raise forms.ValidationError('Выберите файл для загрузки.')
        return file


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
