# users/models.py

import logging  # noqa
# from django.db import models
from django.contrib.auth.models import AbstractUser
from misc import common_classes


class CustomUser(AbstractUser, common_classes.Initable):
    DEFAULT_KEYS = ('username', 'set_password', 'is_staff', 'is_superuser')
    DEFAULT_VALS = (
        ('b3admin', 'b3adminb3admin', True, True),
        ('test', 'test', True, False),
    )

