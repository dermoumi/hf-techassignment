from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^login$', views.login, name='login'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^mailjobs/active$', views.mailjobs_active, name='mailjobs_active'),
    url(r'^mailjobs(?:/all)?$', views.mailjobs_all, name='mailjobs_all'),
    url(r'^mailjobs/rest/get$', views.mailjobs_rest_get, name='mailjobs_rest_get'),
    url(r'^notifications/rest/get$', views.notifications_rest_get, name='notifications_rest_get'),
]