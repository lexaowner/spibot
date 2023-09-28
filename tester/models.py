from django.db import models
from django.utils.translation import gettext as _


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
