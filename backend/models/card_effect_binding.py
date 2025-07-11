from django.db import models

class CardEffectBinding(models.Model):
    card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='effect_bindings')
    trigger = models.ForeignKey('Trigger', on_delete=models.CASCADE)
    effect = models.ForeignKey('Effect', on_delete=models.CASCADE)
    condition = models.ForeignKey('Condition', on_delete=models.SET_NULL, null=True, blank=True)
    restriction = models.ForeignKey('Restriction', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.card.name} | {self.trigger.script_reference} → {self.effect.name}"
