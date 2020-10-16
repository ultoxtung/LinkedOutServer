from django.db import models

from .user import User


class Social(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    social_type = models.CharField(max_length=64)
    social_url = models.CharField(max_length=1024, default='#')
