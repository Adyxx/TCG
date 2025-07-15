from django.db import models
from .character import Character

class CharacterRelationship(models.Model):
    RELATIONSHIP_TYPES = [
        ("PARTNER", "Partner"),
        ("RIVAL", "Rival"),
        ("LOVER", "Lover"),
        ("MENTOR", "Mentor"),
        # etc.
    ]

    source = models.ForeignKey(Character, related_name='relationships_out', on_delete=models.CASCADE)
    target = models.ForeignKey(Character, related_name='relationships_in', on_delete=models.CASCADE)
    relationship_type = models.CharField(max_length=20, choices=RELATIONSHIP_TYPES)

    description = models.TextField(blank=True) 

    class Meta:
        unique_together = ('source', 'target', 'relationship_type')


    def is_valid_partner(main, partner):
        from backend.models import CharacterRelationship
        return CharacterRelationship.objects.filter(
            source=main, target=partner, relationship_type="PARTNER"
        ).exists() and CharacterRelationship.objects.filter(
            source=partner, target=main, relationship_type="PARTNER"
        ).exists()


    def __str__(self):
        return f"{self.source.name} → {self.target.name} ({self.relationship_type})"
