from django.db import models

from .account import Account


class Message(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    content = models.TextField(max_length=1024)
    published_date = models.IntegerField()
