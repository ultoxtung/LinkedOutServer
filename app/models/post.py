from django.db import models
import time

from .user import User
from app.utils import UnixTimestampField


def store_picture(instance, filename: str) -> str:
    extension = filename.split('.')[-1]
    return "post/post_" + "{}.{}".format(instance.id, extension)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1024)
    published_date = UnixTimestampField(auto_created=True)
    post_picture = models.ImageField(
        upload_to=store_picture, default='post/default.jpg')
    interested_users = models.ManyToManyField(
        User, related_name='interest')
