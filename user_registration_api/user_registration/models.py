import email
from django.db import models

class User(models.Model):
    email_address = models.CharField(max_length=255, primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    active = models.BooleanField()