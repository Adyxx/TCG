from django.contrib import admin
from backend.models import Card, Trigger, Effect, Condition, Restriction, CardEffectBinding, Deck, DeckCard, Character


admin.site.register(Character)
admin.site.register(Deck)
admin.site.register(DeckCard)

admin.site.register(Trigger)
admin.site.register(Effect)
admin.site.register(Condition)
admin.site.register(Restriction)
admin.site.register(CardEffectBinding)

class CardEffectBindingInline(admin.TabularInline):
    model = CardEffectBinding
    extra = 1

class CardAdmin(admin.ModelAdmin):
    inlines = [CardEffectBindingInline]

admin.site.register(Card, CardAdmin)

# Register your models here.

