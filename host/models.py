from django.db import models

from django.contrib.auth.models import User


# Create your models here.
class Event(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=50)  # Choices: Created, Running, Ended


class Question(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)


class AnswerChoice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    value = models.IntegerField()
