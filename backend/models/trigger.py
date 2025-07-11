from django.db import models

class Trigger(models.Model):
    script_reference = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.script_reference
