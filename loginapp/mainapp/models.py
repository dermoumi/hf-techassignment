from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, commit=True):
        # Email is mandatory
        if not email:
            raise ValueError(_('An email is required'))

        # Create user and set password
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)

        # Avoid saving if going to be called by create_superuser()
        if commit:
            user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, commit=True):
        # Email is mandatory
        if not email:
            raise ValueError(_('An email is required'))

        # Create superuser, set password and flag as admin
        user = self.create_user(email, password, commit=False)
        user.is_active = True
        user.is_admin = True

        if commit:
            user.save(using=self._db)

        return user

class User(AbstractBaseUser):
    email = models.CharField(_('email'), max_length=100, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    confirmation_token = models.CharField(max_length=32, null=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        # Will not be asking for anything not admin related anyway
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin
