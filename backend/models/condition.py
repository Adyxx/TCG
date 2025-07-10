from django.db import models

class Condition(models.Model):
    name = models.CharField(max_length=100)
    script_reference = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
