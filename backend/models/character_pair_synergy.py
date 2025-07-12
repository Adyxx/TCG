from django.db import models
from .character import Character

class CharacterPairSynergy(models.Model):
    character_a = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='synergy_a')
    character_b = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='synergy_b')

    synergy_ability_ref = models.CharField(max_length=100, blank=True)
    synergy_description = models.TextField(blank=True)

    override_active_ability_ref = models.CharField(max_length=100, blank=True)
    override_passive_ability_ref = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.character_a.name} + {self.character_b.name} Synergy"

    class Meta:
        unique_together = [('character_a', 'character_b')]

    def applies_to(self, char1, char2):
        return {char1.id, char2.id} == {self.character_a.id, self.character_b.id}
