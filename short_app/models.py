from django.contrib.auth.models import User
from django.db import models
from hashids import Hashids
# Create your models here.


class Bookmark(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    url = models.URLField()
    hash_id = models.CharField(max_length=15)
    count = models.IntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created"]


class Click(models.Model):
    user = models.ForeignKey(User)
    link = models.ForeignKey(Bookmark)
    time_click = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-time_click"]
