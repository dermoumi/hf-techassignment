from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.contrib import messages, auth
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from . import forms

# Index view, right now all it does is redirect to user panel
def index(request):
    return signup(request)

# Login view, logs the user in, contrib.auth handles it
def login(request):
    # Check if the user isn't already logged in
    if request.user.is_authenticated():
        return redirect('mainapp:profile')

    return auth_views.login(request, template_name='mainapp/login.html')

# Registers the user into the website
def signup(request):
    # Check if the user is already logged in
    if request.user.is_authenticated():
        return redirect('mainapp:profile')

    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            # Save user to the database
            form.save()

            # Redirect to login page
            messages.success(request, _('You have been successfully registered'))
            return redirect('mainapp:login')
    else:
        form = forms.SignupForm()

    return render(request, 'mainapp/signup.html', {
        'form': form
    })

# Shows the user's profile
def profile(request):
    # Check if the user is actually authenticated
    if not request.user.is_authenticated():
        return auth_views.redirect_to_login(
            request.get_full_path(),
            reverse('mainapp:login', current_app='mainapp')
        )

    return render(request, 'mainapp/profile.html')

# Logs the user out
def logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
        messages.info(request, _('Successfully logged out'))

    return redirect('mainapp:index')