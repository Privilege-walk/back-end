from django.db import models

from user_mgmt.models import AnonymousParticipant
from host.models import AnswerChoice


class Response(models.Model):
    participant = models.ForeignKey(AnonymousParticipant, on_delete=models.CASCADE)
    answer = models.ForeignKey(AnswerChoice, on_delete=models.CASCADE)