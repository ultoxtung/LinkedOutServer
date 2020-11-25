from django.db import models

from .account import Account


class Notification(models.Model):
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    content = models.CharField(max_length=1024)
    account_id = models.IntegerField()
    post_job_id = models.IntegerField()
    comment_id = models.IntegerField()
    published_date = models.IntegerField()
