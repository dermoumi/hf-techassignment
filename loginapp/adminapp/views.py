from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse
from mainapp.models import EmailJob
from django.core import serializers
from . import forms

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
    return render(request, 'adminapp/mailjobs_active.html')

# @user_passes_test(staff_only, login_url='adminapp:login')
def mailjobs_rest_get(request):
    mailjobs = EmailJob.objects.all()
    return HttpResponse(serializers.serialize('json', mailjobs))
