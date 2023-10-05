from django.utils import timezone
from django.db import models
from django.utils.translation import gettext as _
from smart_selects.db_fields import ChainedForeignKey
from django.urls import reverse
from django.contrib.auth.models import User


class Person(models.Model):
    user_name = models.OneToOneField('auth.User', default=True, null=True, on_delete=models.PROTECT, verbose_name="Оператор")
    name = models.CharField(max_length=32, verbose_name='Имя')
    # email = models.EmailField(blank=True, null=True)

    ROLES = [
        ('operator', 'Оператор📞'),
        ('master', 'Мастер🛠'),
        ('admin', 'Воспитатель👶'),
        ('god', 'Боженька🧬'),
        (None, 'Никто'),
    ]

    permissions = models.CharField(max_length=32, choices=ROLES, default=None, null=True, verbose_name='Роль')

    def __str__(self):
        return f"Имя: {self.name} | Кликуха: {self.user_name} | {self.permissions}"

    def get_url(self):
        return reverse('User-name', args=[self.name])

    class Meta:
        verbose_name = 'Задрот'
        verbose_name_plural = 'Задроты'


class Region(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Регион'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Регион'
        verbose_name_plural = 'Регионы'


class District(models.Model):
    region = models.ForeignKey('Region', on_delete=models.CASCADE, verbose_name=_('Регион'))
    name = models.CharField(max_length=64, verbose_name=_('Район'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Район'
        verbose_name_plural = 'Районы'


class Street(models.Model):
    district = models.ForeignKey('District', on_delete=models.CASCADE, verbose_name=_('Район'))
    name = models.CharField(max_length=64, verbose_name=_('name'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Улица'
        verbose_name_plural = 'Улицы'


class House(models.Model):
    street = models.ForeignKey('Street', on_delete=models.CASCADE, verbose_name=_('Улица'))
    name = models.CharField(max_length=64, verbose_name=_('Дом'))
    apartment = models.CharField(max_length=16, blank=True, null=True, verbose_name=('Квартира'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'


class TicketType(models.Model):
    TYPE = [
        ('repair', 'Ремонт'),
        ('settings', 'Настройка'),
        ('transfer', 'Перенос'),
        ('shutdown', 'Отключение'),
        ('installation', 'Установка'),
    ]

    type = models.CharField(max_length=32, choices=TYPE, default='repair', verbose_name="Тип заявки")

    def __str__(self):
        return self.type

    class Meta:
        verbose_name = 'Тип заявки'
        verbose_name_plural = 'Тип заявки'


class Ticket(models.Model):
    # identify = models.CharField(max_length=32, verbose_name=_('identify'))

    district = models.ForeignKey("District", on_delete=models.PROTECT, verbose_name=('Район'))
    street = ChainedForeignKey("Street", chained_field='district', chained_model_field='district', show_all=False)

    # house = models.ForeignKey('House', on_delete=models.CASCADE, verbose_name=_('Дом'))
    house = models.CharField(max_length=16, verbose_name=_('Дом'))
    apartment = models.CharField(max_length=32, verbose_name=_('Квартира'), blank=True, null=True)

    date = models.DateTimeField(editable=True, default=timezone.now, verbose_name="Дата открытия")
    closed_date = models.DateTimeField(editable=True, null=True, blank=True, verbose_name="Дата закрытия")

    completion_date = models.DateTimeField(default=None, null=True, blank=True, editable=True,
                                           verbose_name="Дата выполнения")
    login = models.CharField(blank=True, max_length=15, null=True, verbose_name="Логин")

    first_contact = models.CharField(max_length=13, null=True, verbose_name="Основной номер", default=None)
    second_contact = models.CharField(max_length=13, blank=True, null=True, verbose_name="Доп. номер", default=None)

    comment_master = models.TextField(blank=True, null=True, verbose_name="Комментарий мастера", default=None)
    comment_operator = models.TextField(blank=True, null=True, verbose_name="Комментарий оператора", default=None)

    update = models.DateTimeField(default=timezone.now, editable=False, verbose_name="Дата обновления")
    operator = models.ForeignKey('Person', default=True ,on_delete=models.PROTECT, verbose_name="Оператор")

    type = models.ForeignKey('TicketType', blank=True, null=True, on_delete=models.PROTECT, verbose_name="Тип заявки")

    # master = models.ForeignKey(Human, null=True, blank=True, on_delete=models.PROTECT, verbose_name="Мастер")

    def __str__(self):
        return f'{self.street} | {self.apartment}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def get_url(self):
        return reverse('ticket-form', args=[self.id])

    def get_full_address(self):
        return f'{self.district}, {self.street}, {self.house}'
