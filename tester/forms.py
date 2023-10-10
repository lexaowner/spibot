from django import forms
from django.contrib.auth.forms import UserCreationForm as _UserCreationForm, UserChangeForm as _UserChangeForm

from .models import *


class Addticket(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(Addticket, self).__init__(*args, **kwargs)  # populates the post
        self.fields['master'].queryset = User.objects.filter(groups__name='Мастер')

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
            "operator",
            "priority",
            "comment_operator",
            "comment_master",
        ]


class AddComMaster(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = [
            'comment_master'
        ]


class UserCreationForm(_UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email')


class UserChangeForm(_UserChangeForm):
    class Meta:
        model = User
        fields = ('username', 'email')
