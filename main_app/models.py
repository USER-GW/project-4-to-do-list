from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return f"{self.icon} {self.name}" if self.icon else self.name


class Priority(models.Model):
    level = models.CharField(max_length=10, unique=True)  

    def __str__(self):
        return self.level


class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    priority = models.ForeignKey(Priority, on_delete=models.SET_NULL, null=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title
