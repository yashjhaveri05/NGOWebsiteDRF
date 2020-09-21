from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.shortcuts import reverse

class User(AbstractUser):
    mobile_number = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=150)
    pancard = models.CharField(max_length=10)
    coins = models.IntegerField(default=0)

class Event(models.Model):
    CAUSES = (
        ('Environment Protection', 'Environment Protection'),
        ('Healthcare To Needy', 'Healthcare To Needy'),
        ('Education To Poor/Orphans', 'Education To Poor/Orphans'),
        ('Fighting Human Trafficking', 'Fighting Human Trafficking'),
    )
    created_by = models.ForeignKey(User,related_name="event_creator", on_delete=models.CASCADE)
    volunteers = models.ManyToManyField(User,related_name="volunteers",blank=True)
    title = models.CharField(max_length=75)
    description = models.TextField()
    cause = models.CharField(max_length=50, choices=CAUSES)
    location = models.CharField(max_length=150)
    duration = models.CharField(max_length=20)
    event_timings = models.DateTimeField(default=timezone.now)
    is_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.title

