
from django.db import models

class Restriction(models.Model):
    script_reference = models.CharField(max_length=100, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.description
