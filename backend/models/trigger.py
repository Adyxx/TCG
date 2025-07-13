from django.db import models

ZONES = [
    ('board', 'Board'),
    ('hand', 'Hand'),
    ('deck', 'Deck'),
    ('graveyard', 'Graveyard'),
]

class Trigger(models.Model):
    script_reference = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    zone = models.CharField(
        max_length=20,
        choices=ZONES,
        null=True,
        blank=True,
        help_text="Optional: the zone this trigger applies to (e.g., 'board' for on_friendly_death)"
    )

    def __str__(self):
        return self.script_reference
