import django_filters
from tester.models import *


class TicketFilter(django_filters.FilterSet):
    class Meta:
        modal = Ticket
        fields = [
            'district',
            'street',
            'house',
            'apartment',
            'login',
            'first_contact',
            'second_contact',
            'operator',
            'master',
            'type',
            'priority',
            'status',
        ]
