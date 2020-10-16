from django.db import models

from .school import School
from .user import User


class Education(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    degree = models.CharField(max_length=32)
    major = models.CharField(max_length=255)
