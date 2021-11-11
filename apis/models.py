from django.db import models

# Create your models here.

class AccountManager(models.Model):
    username = models.CharField(max_length=200)
    token = models.CharField(max_length=200)

class EmailAddresses(models.Model):
    email_address = models.CharField(max_length=200)

    def __str__(self):
        return self.email_address