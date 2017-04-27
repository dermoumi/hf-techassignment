from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.db import models

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, commit=True):
        # Username is required
        if not username:
            raise ValueError(_('A username is required'))

        # Email is required
        if not email:
            raise ValueError(_('An email is required'))

        # Create user and set password
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)

        # Avoid saving if going to be called by create_superuser()
        if commit:
            user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password=None, commit=True):
        # Create superuser, set password and flag as admin
        user = self.create_user(username, email, password, commit=False)
        user.is_active = True
        user.is_admin = True

        if commit:
            user.save(using=self._db)

        return user

class User(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True, default='')
    email = models.CharField(max_length=100, unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = MyUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

class EmailJob(models.Model):
    destination = models.CharField(max_length=100)
    status = models.CharField(max_length=10, default='pending')
    retry_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    last_retry_at = models.DateTimeField(null=True)
    celery_id = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.destination
