from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from . import forms

def dashboard(request):
    if not request.user.is_authenticated():
        return auth.views.redirect_to_login(
            request.get_full_path(),
            reverse('adminapp:login', current_app='adminapp')
        )

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