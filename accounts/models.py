from settings import default_translator as _
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('User')
        permissions = ('is_translator', _('User can translate')),
