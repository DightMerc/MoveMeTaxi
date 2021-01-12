from django.db import models

from datetime import datetime

import core.models as CoreModels

import hashlib


class Location(models.Model):

    user = models.ForeignKey(
        CoreModels.CoreUser,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    latitude = models.CharField(
        max_length=255,
        default='',
        blank=False,
        null=False
    )

    longitude = models.CharField(
        max_length=255,
        default='',
        blank=False,
        null=False
    )
