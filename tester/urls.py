from . import views
from django.urls import path

urlpatterns = [
    path('', views.start_page, name='start_page'),
    path('add_ticket/', views.add_ticket, name='add_ticket'),
    path('login/', views.login_cora_2, name='login'),
    path('user/profile/', views.profile, name='profile'),
    path('logout/', views.logout_cora_2, name='logaut'),
    path('edit_ticket/<int:pk>', views.edit_ticket, name='edit_ticket'),
    path('error/', views.error, name='error'),
    path('test/', views.test, name='test'),
    path('full-log-change/<int:pk>', views.log, name='full-log'),
    path('add_comment_master/<int:pk>', views.add_com_master, name='master_comment'),
    path('processing/', views.processing, name='processing'),
    path('shutdown/', views.shutdown, name='shutdown'),
    path('shutdown_master/', views.shutdown_master, name='shutdown_master'),
    path('address/', views.add_address, name='address'),
    path('territory/', views.territory, name='territory'),
    path('edit_news/<int:pk>', views.edit_news, name='edit_news'),
    path('delete_news/<int:pk>', views.delete_news, name='delete_news'),
    path('include_master/', views.include_master, name='include_master'),
]
