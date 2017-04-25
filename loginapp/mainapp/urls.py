from django.conf.urls import url
from . import views

app_name = 'mainapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login, name='login'),
    url(r'^email-notice', views.email_notice, name='email_notice'),
    url(r'^confirm-email', views.confirm_email, name='confirm_email'),
    url(r'^panel/manage', views.panel_manage, name='panel_manage'),
    url(r'^panel/logout', views.panel_logout, name='panel_logout'),
]