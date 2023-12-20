from django.contrib.auth.admin import UserAdmin as _UserAdmin
from django.contrib import admin
from reversion.admin import VersionAdmin
from tester.forms import UserChangeForm, UserCreationForm
from tester.models import *


admin.site.register(News)
admin.site.register(Region)
admin.site.register(House)
admin.site.register(Street)
admin.site.register(District)


class UserAdmin(_UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['username', 'email', ]


admin.site.register(User, UserAdmin)


@admin.register(Ticket)
class TicketAdmin(VersionAdmin):
    pass
