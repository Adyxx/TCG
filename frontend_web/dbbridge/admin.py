
from django.contrib import admin
from backend.models import Deck, Card, DeckCard, Character, Ability

admin.site.register(Character)
admin.site.register(Deck)
admin.site.register(DeckCard)

class CardAdmin(admin.ModelAdmin):
    filter_horizontal = ('abilities',)

admin.site.register(Card, CardAdmin)
admin.site.register(Ability)


# Register your models here.

