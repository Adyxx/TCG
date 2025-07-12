from django.db import models

class Character(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    subtype = models.CharField(max_length=50)

    class_type = models.CharField(max_length=30, choices=[
        ("KNIGHT", "Knight"),
        ("WIZARD", "Wizard"),
        ("BERSERKER", "Berserker"),
        ("PRIEST", "Priest"),
        ("ASSASSIN", "Assassin"),
    ])

    solo_hp = models.IntegerField()
    solo_energy = models.IntegerField()
    partner_hp = models.IntegerField(blank=True, null=True)
    partner_energy = models.IntegerField(blank=True, null=True)

    passive_ability_ref = models.CharField(max_length=100, blank=True)
    passive_description = models.TextField(blank=True)

    active_ability_ref = models.CharField(max_length=100, blank=True)
    active_description = models.TextField(blank=True)

    def __str__(self):
        return self.name
