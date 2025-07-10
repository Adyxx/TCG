from django.db import models

class Trigger(models.Model):
    code = models.CharField(max_length=100, unique=True)  # e.g. "on_death", "on_play", etc.
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code
