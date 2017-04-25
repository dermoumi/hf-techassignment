from django.conf.urls import url
from . import views

app_name = 'mainapp'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.login, name='login'),
    url(r'^email-notice', views.email_notice, name='email_notice'),
    url(r'^confirm-email', views.confirm_email, name='confirm_email'),
    url(r'^accounts/profile', views.accounts_profile, name='accounts_profile'),
    url(r'^accounts/logout', views.accounts_logout, name='accounts_logout'),
]