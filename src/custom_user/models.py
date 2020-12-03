import pytz
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from custom_user.managers import CustomUserManager


class CLGroup(models.Model):
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=254, blank=True, null=True)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    groups = models.ManyToManyField(
        to=CLGroup,
        blank=True,
        related_name="users"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = CustomUserManager()

    class Meta:
        db_table = 'auth_user'
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ('-created_at', )

    def __str__(self):
        return str(self.get_username())

    def save(self, *args, **kwargs):
        # If email is empty string '', convert it to NULL (None)
        if self.email == '':
            self.email = None
        return super().save(*args, **kwargs)

    @property
    def is_operator(self):
        return self.is_staff
    
    @property
    def is_client(self):
        return not self.is_staff
