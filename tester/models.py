from django.utils import timezone
from django.db import models
from django.utils.translation import gettext as _
from smart_selects.db_fields import ChainedForeignKey
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, Permission

from spibot import settings


class User(AbstractUser):
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    is_superuser = models.BooleanField(_('superuser status'), default=False, help_text=_(
        'Designates that this user has all permissions without explicitly assigning them.'))
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_(
        'Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    phone_number = models.CharField(max_length=32, blank=True, null=True, verbose_name=_('phone number'))

    class Meta:
        ordering = ('id',)

        permissions = [
            ("operator", "Can add ticket,change, change yourself profile"),
            ("master", "Can closed ticked,change owner, change yourself profile"),
        ]

    def __str__(self):
        return self.username

    @staticmethod
    def generate_string(length=12):
        import string
        import random
        password = []
        for i in range(length):
            randomizer = random.choice(string.ascii_letters + string.digits)
            password.append(randomizer)
        return "".join(password)


# class User(models.Model):
#     user_name = models.OneToOneField('auth.User', default=True, null=True, on_delete=models.PROTECT, verbose_name="Чел")
#     name = models.CharField(max_length=32, verbose_name='Имя')
#
# ROLES = [
#     ('operator', 'Оператор📞'),
#     ('master', 'Мастер🛠'),
#     ('admin', 'Воспитатель👶'),
#     ('god', 'Боженька🧬'),
#     (None, 'Никто'),
# ]
#
# permissions = models.CharField(max_length=32, choices=ROLES, default=None, blank=True, null=True,
#                                verbose_name='Роль')
#
#     STATUS = [
#         (None, 'New'),
#         ("Уже в базе", 'Old')
#     ]
#
#     status = models.CharField(max_length=32, choices=STATUS, default=None, blank=True, null=True, verbose_name='Статус')
#
#     def __str__(self):
#         return f"Имя: {self.name} | Кликуха: {self.user_name} | {self.permissions}"
#
#     def get_url(self):
#         return reverse('User-name', args=[self.name])
#
#     class Meta:
#         verbose_name = 'Задрот'
#         verbose_name_plural = 'Задроты'
#
#         permissions = [
#             ("operator", "Can add ticket,change, change yourself profile"),
#             ("master", "Can closed ticked,change owner, change yourself profile"),
#         ]


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
    # master = models.ForeignKey('User')
    street = models.ForeignKey('Street', on_delete=models.CASCADE, verbose_name=_('Улица'))
    name = models.CharField(max_length=64, verbose_name=_('Дом'))
    apartment = models.CharField(max_length=16, blank=True, null=True, verbose_name=('Квартира'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дом'
        verbose_name_plural = 'Дома'


class Ticket(models.Model):
    district = models.ForeignKey("District", on_delete=models.PROTECT, verbose_name=('Район'))
    street = ChainedForeignKey("Street", chained_field='district', chained_model_field='district', show_all=False)

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
    operator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Оператор",related_name='operator_tickets',null=True, blank=True,  default=None)

    master = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, verbose_name="Мастер",related_name='mater_tickets')

    TYPE = [
        ('Ремонт', 'Ремонт'),
        ('Настройка', 'Настройка'),
        ('Перенос', 'Перенос'),
        ('Отключение', 'Отключение'),
        ('Установка', 'Установка'),
    ]

    type = models.CharField(max_length=13, choices=TYPE, verbose_name="Тип заявки")

    PRIORITY = [
        ('Обычный', 'Обычный'),
        ('Срочный', 'Срочный'),
        ('Корпоративный', 'Корпоративный'),
    ]

    priority = models.CharField(max_length=13, choices=PRIORITY, default="Обычный", verbose_name="Приоритет")

    STATUS = [
        ('open', 'Открыта'),
        ('closed', 'Закрыта')
    ]

    status = models.BooleanField(choices=[(True, 'Открыта'), (False, 'Закрыта')], default=True)

    def __str__(self):
        return f'{self.street} | {self.apartment}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    def get_url(self):
        return reverse('ticket-form', args=[self.id])

    def get_full_address(self):
        return f'{self.district}, {self.street}, {self.house}'
