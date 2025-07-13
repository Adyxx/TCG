from django.db import models
from django.core.exceptions import ImproperlyConfigured

class Effect(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    script_reference = models.CharField(max_length=100)
    requires_value = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_executable(self):
        from backend.registry.effects import EFFECT_REGISTRY
        effect_entry = EFFECT_REGISTRY.get(self.script_reference)
        if not effect_entry:
            raise ImproperlyConfigured(f"No effect function found for script_reference '{self.script_reference}'")
        return effect_entry["func"], effect_entry["target"]
