from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from mainapp.models import EmailJob
from django.core import serializers
from django.core.paginator import Paginator
from . import forms, models

def staff_only(user):
    return user.is_authenticated() and user.is_staff

@user_passes_test(staff_only, login_url='adminapp:login')
def dashboard(request):
    return render(request, 'adminapp/dashboard.html', {})

def login(request):
    if request.user.is_authenticated() and request.user.is_staff:
        return redirect('adminapp:dashboard')

    if request.method == 'POST':
        form = forms.AdminLoginForm(request.POST)
        if form.is_valid():
            # Log out the current non-admin user, if any
            if request.user.is_authenticated():
                auth.logout(request)

            # Login the user
            auth.login(request, form.authenticated_user())

            # Go to the dashboard
            return redirect('adminapp:dashboard')
    else:
        form = forms.AdminLoginForm()

    return render(request, 'adminapp/login.html', {
        'form': form
    })

def logout(request):
    if request.user.is_authenticated() and request.user.is_staff:
        auth.logout(request)
        messages.info(request, _('Successfully logged out'))

    return redirect('adminapp:login') # Or to the main site?

@user_passes_test(staff_only, login_url='adminapp:login')
def mailjobs_all(request):
    return render(request, 'adminapp/mailjobs_all.html')

@user_passes_test(staff_only, login_url='adminapp:login')
def mailjobs_active(request):
    mail_jobs = EmailJob.objects.filter(status__in=['pending', 'started', 'retrying']).order_by('-created_at')

    return render(request, 'adminapp/mailjobs_active.html', {
        'initial_entries': serializers.serialize('json', mail_jobs)
    })

@user_passes_test(staff_only, login_url='adminapp:login')
def mailjobs_rest_get(request):
    if request.method == 'POST':
        page_size = int(request.POST.get('page_size', 10))
        page = request.POST.get('page', 1)
        order_by = request.POST.get('sort_by', 'created_at')
        order_dir = '' if request.POST.get('sort_dir', 'asc') == 'asc' else '-'

        mail_jobs = EmailJob.objects.order_by(order_dir + order_by)
        paginator = Paginator(mail_jobs, page_size)

        page_jobs = serializers.serialize('json', paginator.page(page).object_list)
        json_output = '{"total_count": %i, "entries": %s}' % (mail_jobs.count(), page_jobs)

    else:
        json_output = ''

    return HttpResponse(json_output, content_type="application/json")

@user_passes_test(staff_only, login_url='adminapp:login')
def notifications_rest_get(request):
    if request.method == 'POST':
        load_fields = ('unread', 'notification',)
        notifications = models.UserNotification.objects.filter(user_id=request.user.pk, unread=True)\
            .order_by('-notification__time') # Can't order by notification time for some reason, by id plays nicely too
        notifications_count = notifications.count()

        # If number of unread notifications is less than six
        if notifications_count < 6:
            more_notifications = models.UserNotification.objects.filter(user_id=request.user.pk, unread=False)\
                .order_by('-notification__time')
            more_notifications = more_notifications[:6 - notifications_count]
            notifications = list(notifications) + list(more_notifications)

        json_output = serializers.serialize('json', notifications, fields=load_fields, use_natural_foreign_keys=True)
    else:
        json_output = ''

    return HttpResponse(json_output, content_type="application/json")