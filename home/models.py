from django.db import models

# Create your models here.

class Signup(models.Model):
    email = models.EmailField(unique=True)