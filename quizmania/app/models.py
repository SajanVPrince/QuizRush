from django.db import models
from django.contrib.auth.models import *
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Question(models.Model):
    text = models.CharField(max_length=255)
    option_a = models.CharField(max_length=100)
    option_b = models.CharField(max_length=100)
    option_c = models.CharField(max_length=100)
    option_d = models.CharField(max_length=100)
    correct_answer = models.CharField(max_length=1)  # 'A', 'B', 'C', or 'D'
    difficulty = models.IntegerField(default=1)  # Difficulty level
    time = models.IntegerField(default=60)  # Time limit in seconds

@receiver(pre_save, sender=Question)
def set_time_based_on_difficulty(sender, instance, **kwargs):
    if instance.difficulty == 1:
        instance.time = 60
    elif instance.difficulty == 2:
        instance.time = 30
    elif instance.difficulty == 3:
        instance.time = 15

    def __str__(self):
        return self.text

class Player(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email=models.EmailField()
    dob=models.DateField()
    score = models.IntegerField(default=0)
    lives = models.IntegerField(default=3)

    def __str__(self):
        return self.name