from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Logins(models.Model):
      first_name = models.CharField(max_length=255)
      last_name = models.CharField(max_length=255)
      email = models.CharField(max_length=255)
      password = models.CharField(max_length=255)
