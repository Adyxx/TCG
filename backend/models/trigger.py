from django.db import models

class Trigger(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code
