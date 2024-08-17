from django.db import models

class Account(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    owner = models.ForeignKey(to='user.User', on_delete=models.CASCADE, null=True)

    account_number = models.CharField(max_length=24)
    balance = models.IntegerField()
