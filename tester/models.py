from django.utils import timezone
from django.db import models
from django.utils.translation import gettext as _
from smart_selects.db_fields import ChainedForeignKey

class Human(models.Model):
    user_name = models.CharField(max_length=32)
    email = models.EmailField()

class Region(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('name'))

    def __str__(self):
        return self.name


class District(models.Model):
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name=_('region'))
    name = models.CharField(max_length=64, verbose_name=_('name'))

    def __str__(self):
        return self.name


class Street(models.Model):
    district = models.ForeignKey('District', on_delete=models.CASCADE, verbose_name=_('district'))
    name = models.CharField(max_length=64, verbose_name=_('name'))

    def __str__(self):
        return self.name


class House(models.Model):
    street = models.ForeignKey('Street', on_delete=models.CASCADE, verbose_name=_('street'))
    name = models.CharField(max_length=64, verbose_name=_('name'))

    def __str__(self):
        return self.name


class Ticket(models.Model):
    identify = models.CharField(max_length=32, verbose_name=_('identify'))
    username = models.CharField(max_length=32, verbose_name=_('username'))

    house = models.ForeignKey('House', on_delete=models.CASCADE, verbose_name=_('house'))
    date = models.DateTimeField(editable=True, default=timezone.now, verbose_name="Дата открытия")

    closed_date = models.DateTimeField(editable=True, null=True, blank=True, verbose_name="Дата закрытия")
    completion_date = models.DateTimeField(default=None, null=True, blank=True, editable=True,verbose_name="Дата выполнения")

    login = models.CharField(blank=True, max_length=15, null=True, verbose_name="Логин")
    first_contact = models.CharField(max_length=13, null=True, verbose_name="Основной номер", default=None)

    second_contact = models.CharField(max_length=13, blank=True, null=True, verbose_name="Доп. номер", default=None)
