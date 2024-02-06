from django.utils import timezone
from django.db import models
from django.utils.translation import gettext as _
from smart_selects.db_fields import ChainedForeignKey
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, Permission


from spibot import settings


class User(AbstractUser):
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    is_superuser = models.BooleanField(_('superuser status'), default=False, help_text=_('Designates that this user has all permissions without explicitly assigning them.'))
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False,help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    phone_number = models.CharField(max_length=32, blank=True, null=True, verbose_name=_('phone number'))
    telegram_id = models.CharField(max_length=10, blank=True, null=True, verbose_name=_('telegram_id'))

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

        ordering = ('id',)

        permissions = [
            ("operator", "Can add ticket, change, change yourself profile"),
            ("master", "Can closed ticked, change owner, change yourself profile"),
            ("dispatcher", "Can add ticket, change, change yourself profile, add news, change news, change ticket status")
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


class TicketManager(models.Manager):
    def get_queryset_true(self):
        return super().get_queryset().filter(deleted=False).order_by("-date")

    def get_queryset_none(self):
        return super().get_queryset().filter(status=None).order_by("-date")

    def get_master(self, id):
        return super().get_queryset().filter(master=id)

    def get(self, id):
        return super().get_queryset().get(id=id)


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
    name = models.CharField(max_length=64, verbose_name=_('Улица'))

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


class Ticket(models.Model):
    objects = TicketManager()

    district = models.ForeignKey("District", on_delete=models.PROTECT, verbose_name=_('Район'))
    street = ChainedForeignKey("Street", chained_field='district', chained_model_field='district', show_all=False,
                               verbose_name=_('Улица'))
    house = models.CharField(max_length=16, verbose_name=_('Дом'))
    apartment = models.CharField(max_length=32, verbose_name=_('Кв'), blank=True, null=True)
    date = models.DateTimeField(editable=True, default=timezone.now, verbose_name="Дата открытия")
    date_change = models.DateTimeField(editable=True, default=timezone.now, verbose_name="Дата измененя")
    closed_date = models.DateTimeField(editable=True, null=True, blank=True, verbose_name="Дата закрытия")
    completion_date = models.DateTimeField(default=None, null=True, blank=True, editable=True, verbose_name="Дата выполнения")
    login = models.CharField(blank=True, max_length=15, null=True, verbose_name="Логин")
    first_contact = models.CharField(max_length=13, null=True, verbose_name="Основной номер", default=None)
    second_contact = models.CharField(max_length=13, blank=True, null=True, verbose_name="Доп. номер", default=None)
    comment_master = models.TextField(blank=True, null=True, verbose_name="Комментарий мастера", default=None)
    comment_operator = models.TextField(blank=True, null=True, verbose_name="Комментарий оператора", default=None)
    operator = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Оператор",
                                 related_name='operator_tickets', null=True, blank=True, default=None)
    master = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, verbose_name="Мастер",
                               related_name='mater_tickets')

    TYPE = [
        ('Ремонт', 'Ремонт'),
        ('Настройка', 'Настройка'),
        ('Перенос', 'Перенос'),
        ('Включение', 'Включение'),
        ('Отключение', 'Отключение'),
        ('Установка', 'Установка'),
        ('Тюнер', 'Тюнер'),
    ]

    type = models.CharField(max_length=13, choices=TYPE, verbose_name="Тип заявки")

    PRIORITY = [
        ('Обычный', 'Обычный'),
        ('Срочный', 'Срочный'),
        ('Корпоративный', 'Корпоративный'),
    ]

    priority = models.CharField(max_length=13, choices=PRIORITY, default="Обычный", verbose_name="Приоритет")
    status = models.BooleanField(choices=[(True, 'Открыта'), (False, 'Закрыта'), (None, 'В обработке')], null=True,
                                 blank=True, default=None,
                                 verbose_name="Статус", )
    cause = models.BooleanField(choices=[(True, '----------'), (None, 'Выполнена'), (False, 'Не дозвон')], null=True,
                                blank=True, default=None,
                                verbose_name="Причина закрытия", )
    user_change = models.CharField(max_length=24, null=True, blank=True, verbose_name="Изменил")
    viewed = models.BooleanField(choices=[(True, 'Просмотрено'), (False, 'Не просмотрено')], null=True,
                                blank=True, default=False,
                                verbose_name="Статус тикета", )
    deleted = models.BooleanField(choices=[(True, 'Удаленна'), (False, 'Активна'), ], null=True,
                                  blank=True, default=False,
                                  verbose_name="Статус_deleted", )

    def __str__(self):
        return f'{self.street} | {self.house} | {self.apartment}| {self.status}'

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

    #
    # def delete(self, using=None, keep_parents=False):
    #     self.deleted
    def get_url(self):
        return reverse('ticket-form', args=[self.id])

    def get_full_address(self):
        return f'{self.district}, {self.street}, {self.house}'


class News(models.Model):
    title = models.TextField(max_length=25, null=True, blank=True, verbose_name="Заголовок")
    text = models.TextField(max_length=255, verbose_name="Текст")
    date = models.DateTimeField(editable=True, default=timezone.now, verbose_name="Дата открытия")

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return self.title


class Shutdown(models.Model):
    street = models.CharField(max_length=40, blank=True, null=True, verbose_name=_('Улица'))
    house = models.CharField(max_length=16, blank=True, null=True, verbose_name=_('Дом'))
    apartment = models.CharField(max_length=32, blank=True, null=True, verbose_name=_('Кв'))
    date = models.DateTimeField(editable=True, default=timezone.now, verbose_name="Дата открытия")
    date_change = models.DateTimeField(editable=True, default=timezone.now, verbose_name="Дата измененя")
    closed_date = models.DateTimeField(editable=True, null=True, blank=True, verbose_name="Дата закрытия")
    master = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Мастер", related_name='mater_shutdown')
    completion = models.BooleanField(choices=[(True, 'Выполнено'), (False, 'Не Выполнено')], null=True, blank=True,verbose_name="Выполнение", default=False)
    deleted = models.BooleanField(choices=[(True, 'Удаленна'), (False, 'Активна'), ], null=True,blank=True, default=False,verbose_name="Статус_deleted")
    comment = models.CharField(max_length=250,blank=True, null=True, verbose_name="Комментарий мастера", default=None)
    file = models.FileField(verbose_name='Файл отключки')

    class Meta:
        verbose_name = 'Отключки'
        verbose_name_plural = 'Отключки'

    def __str__(self):
        return f'Отключка {self.master.first_name} Адрес: {self.street} Дом: {self.house} Кв: {self.apartment}'

    def get_display_name(self):
        # Логика для получения строкового представления объекта
        return f"{self.master} - {self.file}"
