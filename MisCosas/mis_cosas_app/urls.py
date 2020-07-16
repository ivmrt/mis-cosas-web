from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('logout', views.log_out),
    path('login', views.log_in),
    path('usuarios', views.usuarios),
    path('registro', views.new_user),
    path('info', views.info),
    path('alimentadores', views.alimentadores),
    path('usuarios/<str:id_usuario>', views.usuario),
    path('alimentadores/<str:id_alimentador>', views.alimentador),
    path('item/<str:id_item>', views.item),
]
