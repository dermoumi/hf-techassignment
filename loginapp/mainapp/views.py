from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.urls import reverse

# Index view, right now all it does is redirect to user panel
def index(request):
    return redirect('mainapp:accounts_profile')

# Login view, logs the user in, contrib.auth handles it
def login(request):
    # TODO: Check if the user isn't already logged in

    return auth_views.login(request, template_name='mainapp/login.html')

def email_notice(request):
    # TODO: Implement email notice
    pass

def confirm_email(request):
    # TODO: Implement email confirmation
    pass

# Shows the user's profile
def accounts_profile(request):
    if request.user.is_anonymous:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(
            request.get_full_path(),
            reverse('mainapp:login', current_app='mainapp')
        )
    elif request.user.is_staff:
        return redirect('admin:index')

    return render(request, 'mainapp/accounts_profile.html')

# Logs the user out
def accounts_logout(request):
    if not request.user.is_anonymous:
        auth_views.logout(request)
        messages.info(request, _('Successfully disconnected'))

    return redirect('mainapp:index')
