from . import views
from django.urls import path

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('add_ticket/', views.add_ticket, name='add_ticket'),
    path('login/', views.login_cora_2, name='login'),
    path('user/profile/', views.profile, name='profile'),
    path('logout/', views.logout_cora_2, name='logaut'),
    path('edit_ticket/<int:id>', views.EditTicketForm, name='edit_ticket'),
    path('error/', views.error, name='error'),

]
