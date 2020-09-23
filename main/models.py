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

class Donation(models.Model):
    PAYMENT_METHOD = (
        ('BankTransfer', 'BankTransfer'),
        ('PayTM', 'PayTM'),
        ('GooglePay', 'GooglePay'),
        ('CreditCard', 'CreditCard'),
        ('DebitCard', 'DebitCard')
    )
    donated_by = models.ForeignKey(User,related_name="donor", on_delete=models.CASCADE)
    amount_donated = models.FloatField()
    donated_on = models.DateTimeField(default=timezone.now, editable=False)
    bank_name = models.CharField(max_length=25)
    bank_branch = models.CharField(max_length=50)
    payment_method = models.CharField(max_length=12, choices=PAYMENT_METHOD)

    def __str__(self):
        return self.donated_by.username

class Redeem(models.Model):
    title = models.CharField(max_length=30)
    brand = models.CharField(max_length=30)
    description = models.TextField()
    price = models.IntegerField(default=0)
    image = models.ImageField(default='default1.png', upload_to='images/')
    created = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Achievement(models.Model):
    event = models.OneToOneField(Event,on_delete=models.CASCADE)
    details = models.TextField()
    awards = models.TextField(blank=True)
    funds_used = models.FloatField()
    image = models.ImageField(default='default.png', upload_to='images/')

    def __str__(self):
        return self.event.title
        
