from django.db import models

from .user import User
from .post import Post
from app.utils import UnixTimestampField


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=1024)
    published_date = UnixTimestampField(auto_created=True)
