from django.db import models

class Ability(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    script_reference = models.CharField(max_length=100, help_text="Code logic ref name, e.g. `apply_haste_effect`")

    def __str__(self):
        return self.name
