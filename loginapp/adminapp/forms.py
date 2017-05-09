from django import forms
from django.utils.translation import ugettext_lazy as _

class AdminLoginForm(forms.Form):
    username = forms.CharField(label=_('Username'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    def clean(self):
        from django.contrib import auth

        cleaned_data = super(AdminLoginForm, self).clean()

        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is None or not user.is_active:
            self.add_error(forms.forms.NON_FIELD_ERRORS, _('Username or password are incorrect'))

        if user is not None and not user.is_staff:
            self.add_error(forms.forms.NON_FIELD_ERRORS, _('Only staff can log in to the administration panel'))

        self.__authenticated_user = user

        return cleaned_data

    def authenticated_user(self):
        return self.__authenticated_user