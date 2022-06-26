from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField()
    auth_provider = models.CharField(
        max_length=255, blank=False,
        null=False, default='email'
    )
