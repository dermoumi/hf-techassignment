from django.shortcuts import render, redirect

# Index view, right now all it does is redirect to user panel
def index(request):
    return redirect('mainapp:panel_manage')

def login(request):
    # TODO: Implement login page
    pass

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
