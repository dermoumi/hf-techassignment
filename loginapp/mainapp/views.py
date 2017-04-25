from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views

# Index view, right now all it does is redirect to user panel
def index(request):
    return redirect('mainapp:panel_manage')

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

def panel_manage(request):
    # TODO: Impelement panel manage
    pass

def panel_logout(request):
    # TODO: Implement panel logout
    pass
