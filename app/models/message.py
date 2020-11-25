from django.db import models

from .account import Account


class Message(models.Model):
    sender = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name='receiver')
    type = models.CharField(max_length=10)
    content = models.TextField(max_length=1024)
    published_date = models.IntegerField()
