from django.db import models

class Character(models.Model):
    name = models.CharField(max_length=100)
    color = models.CharField(max_length=20)
    subtype = models.CharField(max_length=50)

    solo_hp = models.IntegerField()
    solo_energy = models.IntegerField()
    solo_passive = models.TextField()

    partner_hp = models.IntegerField()
    partner_energy = models.IntegerField()
    partner_passive = models.TextField()

    def __str__(self):
        return self.name
