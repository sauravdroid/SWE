from django.conf.urls import url
from . import views

app_name = 'rest'

urlpatterns = [
    url(r'^$', views.get_users, name='get_users'),
    url(r'^all_users/$', views.all_users, name='all_users'),
    url(r'^forms/$', views.all_users, name='forms'),
]
