from django.db import models


from .account import Account
from .specialty import Specialty
from .user import User


def store_picture(instance, filename: str) -> str:
    extension = filename.split('.')[-1]
    return "profile/company_" + "{}.{}".format(instance.account.username, extension)


class Company(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    website = models.TextField(null=True)
    description = models.TextField(null=True)
    profile_picture = models.ImageField(
        upload_to=store_picture, default='profile/company_default.jpg')

    followers = models.ManyToManyField(
        User, related_name='company_followed')
    specialties = models.ManyToManyField(Specialty)
