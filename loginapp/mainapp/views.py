from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from . import forms

# Index view, right now all it does is redirect to user panel
def index(request):
    return redirect('mainapp:signup')

# Login view, logs the user in, contrib.auth handles it
def login(request):
    # TODO: Check if the user isn't already logged in

    return auth_views.login(request, template_name='mainapp/login.html')

# Registers the user into the website
def signup(request):
    # Check if the user is already logged in
    response = filter_login(request)
    if response: return response

    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            # form.save()

            messages.success(request, _('You have been successfully registered'))
            return redirect('mainapp:login')
    else:
        form = forms.SignupForm()

    return render(request, 'mainapp/signup.html', {
        'form': form
    })

# Shows the user's profile
def profile(request):
    if request.user.is_anonymous:
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(
            request.get_full_path(),
            reverse('mainapp:login', current_app='mainapp')
        )
    elif request.user.is_staff:
        return redirect('admin:index')

    return render(request, 'mainapp/profile.html')

# Logs the user out
def logout(request):
    if not request.user.is_anonymous:
        auth_views.logout(request)
        messages.info(request, _('Successfully logged out'))

    return redirect('mainapp:index')

def filter_login(request):
    user = request.user
    if user.is_staff:
        return redirect('admin:index')
    elif not user.is_anonymous:
        return redirect('mainapp:profile')