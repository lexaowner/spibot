from . import views
from . import cora_bot
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

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
    path('delete_obj/<int:pk>', views.delete_obj, name='delete_obj'),
    path('delete_shutdown/<int:pk>', views.del_shutdown, name='del_shutdown'),
    path('include_master/', views.include_master, name='include_master'),###########
    path('info/', views.info, name='info'),
    path('login_telegram/', views.login_in_telegram, name='login_telegram'),
    # path('start_bot/', views.bot, name='start_bot'),
    # path('set_webhook/', views.set_webhook, name='set_webhook')
]
