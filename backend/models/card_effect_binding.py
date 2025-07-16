from django.core.exceptions import ValidationError
from django.db import models

TARGET_SPEC_CHOICES = [
    ("enemy:board", "Enemy Board"),
    ("enemy:hero", "Enemy Hero"),
    ("enemy:board_or_hero", "Enemy Board or Hero"),
    ("friendly:board", "Friendly Board"),
    ("self", "Self"),
    ("any", "Any Target"),
]


class CardEffectBinding(models.Model):
    card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='effect_bindings')
    trigger = models.ForeignKey('Trigger', on_delete=models.CASCADE)
    effect = models.ForeignKey('Effect', on_delete=models.CASCADE)
    condition = models.ForeignKey('Condition', on_delete=models.SET_NULL, null=True, blank=True)
    restriction = models.ForeignKey('Restriction', on_delete=models.SET_NULL, null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    target_spec = models.CharField(max_length=50, choices=TARGET_SPEC_CHOICES, blank=True, null=True, help_text="Targeting behavior for this effect (used if effect requires target)")
    
    def __str__(self):
        return f"{self.card.name} | {self.trigger.script_reference} → {self.effect.name}"

    def clean(self):
        if self.effect.requires_value and self.value is None:
            raise ValidationError(f"Effect '{self.effect.name}' requires a value, but none was provided.")
        if not self.effect.requires_value and self.value is not None:
            raise ValidationError(f"Effect '{self.effect.name}' does not accept a value, but one was provided.")
        
        if self.effect.requires_target and not self.target_spec:
            raise ValidationError(f"Effect '{self.effect.name}' requires a target, but no target_spec was provided.")
        if not self.effect.requires_target and self.target_spec:
            raise ValidationError(f"Effect '{self.effect.name}' does not accept a target, but target_spec was provided.")
