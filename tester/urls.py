from . import views
from django.urls import path

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('add_ticket/', views.add_ticket, name='add_ticket'),
]
