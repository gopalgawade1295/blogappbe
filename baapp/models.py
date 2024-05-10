from django.db import models
from django.contrib.auth.models import User
import uuid
from django.conf import settings


class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    article = models.TextField(null=True, blank=True)
    author = models.CharField(max_length=100, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now_add=True)
    uid = models.UUIDField(
        primary_key=True, editable=False, default=uuid.uuid4)

    def __str__(self):
        return self.title
