from django.db import models

class User(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    code_melli = models.CharField(max_length=10)