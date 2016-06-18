from django.contrib.auth.models import User
from django.db import models


class Bookmark(models.Model):
    title = models.CharField(max_length=60)
    description = models.TextField()
    url = models.URLField()
    created = models.DateTimeField(auto_now_add=True)
    hash_id = models.CharField(max_length=10, null=True)
    count = models.IntegerField(default=0)
    user = models.ForeignKey(User)

    class Meta:
        ordering = ["-created"]

    def __str__(self):
        return self.title


class Click(models.Model):
    link = models.ForeignKey(Bookmark)
    time_click = models.DateTimeField()

    class Meta:
        ordering = ["-time_click"]
