from django import forms
from django.utils.translation import ugettext_lazy as _

from . import models

class SignupForm(forms.ModelForm):
    email = forms.EmailField(label=_('Email'))
    password = forms.CharField(label=_('Password'), widget=forms.PasswordInput)
    password_confirmation = forms.CharField(label=_('Password confirmation'), widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ('username', 'email',)

    def clean_password_confirmation(self):
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')

        # Check if both passwords are identical
        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError(_('Passwords need to be identical'))

        return password_confirmation

    def save(self, commit=True):
        # Save hashed, salted password
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data.get('password'))
        user.is_active = True
        
        # Start email task
        from . import tasks
        tasks.send_email(form.cleaned_data.get('email'))

        if commit:
            user.save()

        return user
