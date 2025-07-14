from django.db import models

class Subtype(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Faction(models.Model):
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

class Character(models.Model):
    CLASS_TYPES = [
        ("KNIGHT", "Knight"),
        ("WIZARD", "Wizard"),
        ("BERSERKER", "Berserker"),
        ("PRIEST", "Priest"),
        ("ASSASSIN", "Assassin"),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField(blank=True, null=True)
    height_cm = models.FloatField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    short_bio = models.TextField(blank=True)
    backstory = models.TextField(blank=True)

    image = models.ImageField(upload_to='characters/', blank=True, null=True)
    model_file_path = models.CharField(max_length=200, blank=True)

    faction = models.ForeignKey(Faction, on_delete=models.SET_NULL, null=True, blank=True)
    subtypes = models.ManyToManyField(Subtype, related_name='characters', blank=True)

    class_type = models.CharField(max_length=30, choices=CLASS_TYPES)

    solo_hp = models.IntegerField()
    partner_hp = models.IntegerField(blank=True, null=True)

    passive_ability_ref = models.CharField(max_length=100, blank=True)
    passive_description = models.TextField(blank=True)

    active_ability_ref = models.CharField(max_length=100, blank=True)
    active_description = models.TextField(blank=True)

    partner_ability_ref = models.CharField(max_length=100, blank=True)
    partner_description = models.TextField(blank=True)

    solo_bonus_ref = models.CharField(max_length=100, blank=True)
    solo_bonus_description = models.TextField(blank=True)

    deck_restriction_ref = models.CharField(max_length=100, blank=True)
    deck_restriction_description = models.TextField(blank=True)

    def __str__(self):
        return self.name
