from django.db import models

class Effect(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    script_reference = models.CharField(max_length=100)

    def __str__(self):
        return self.name
