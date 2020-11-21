from django.db import models

from .account import Account


class Follow(models.Model):
    sender = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='following')
    receiver = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='followers')
