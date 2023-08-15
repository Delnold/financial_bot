from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('messages', views.messages, name='messages'),
    path('callback_query', views.callback_query, name='callback_query'),
    re_path(r'^commands.*$', views.commands, name='commands'),
]
