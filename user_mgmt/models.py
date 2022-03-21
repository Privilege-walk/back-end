from django.db import models
from random import randint

from host.models import Event


# Create your models here.
class AnonymousParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    unique_code = models.CharField(max_length=4, blank=True)

    def save(self, *args, **kwargs):
        self.unique_code = self.generate_unique_code()
        super(AnonymousParticipant, self).save(*args, **kwargs)

    def generate_unique_code(self):
        generated_code = ''
        exists = True

        while (exists):
            for i in range(4):
                generated_code += chr(ord('A') + randint(0, 25))

            n_prev = len(AnonymousParticipant.objects.filter(unique_code=generated_code))

            if n_prev == 0:
                break

        return generated_code
