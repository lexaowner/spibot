from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as _UserAdmin

from tester.forms import UserChangeForm, UserCreationForm
from tester.models import *

admin.site.register(Region)
admin.site.register(House)
admin.site.register(Street)
admin.site.register(District)
admin.site.register(Ticket)


class UserAdmin(_UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['username', 'email', ]


admin.site.register(User, UserAdmin)


