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
admin.site.register(Shutdown)


class UserAdmin(_UserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = ['username', 'email', 'telegram_id']  # Добавлено поле 'telegram_id'

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'telegram_id'),
        }),
    )

    fieldsets = _UserAdmin.fieldsets + (
        (None, {'fields': ('telegram_id',)}),
    )


admin.site.register(User, UserAdmin)


@admin.register(Ticket)
class TicketAdmin(VersionAdmin):
    pass
