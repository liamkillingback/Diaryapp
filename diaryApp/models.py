from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Task(models.Model):
    task = models.CharField(max_length=25)

    def __str__(self):
        return self.task
    def serialize(self):
        return {
            "task": self.task,
            "id": self.id
        }


class Entry(models.Model):
    main = models.BooleanField(default=False)
    body = models.CharField(max_length=500, blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    tasks = models.ManyToManyField(Task, related_name="tasks", blank=True, null=True)
    date = models.CharField(max_length=50, null=True, blank=True)
    weekday = models.CharField(max_length=50, null=True, blank=True)
    completed_tasks = models.ManyToManyField(Task, related_name="completed_tasks", blank=True)

    def __str__(self):
        return f"{self.owner.username},{self.date}"
    
    def serialize(self):
        return {
            "body": self.body,
            "id": self.id
        }

class CompletedTask(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    task = models.ManyToManyField(Task, blank=True)
    completion_date = models.DateTimeField(auto_now_add=True)

    