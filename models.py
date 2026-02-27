
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.FloatField()  # in cm
    weight = models.FloatField()  # in kg

    def __str__(self):
        return self.name


class DailyCalorie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=100)
    calorie_consumed = models.FloatField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.item_name