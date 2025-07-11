from django.contrib import admin
from django.utils.html import format_html, format_html_join
from backend.models import (
    Card,
    Trigger,
    Effect,
    Condition,
    Restriction,
    CardEffectBinding,
    Deck,
    DeckCard,
    Character,
)

admin.site.register(Character)
admin.site.register(Trigger)
admin.site.register(Effect)
admin.site.register(Condition)
admin.site.register(Restriction)
admin.site.register(CardEffectBinding)

class CardEffectBindingInline(admin.TabularInline):
    model = CardEffectBinding
    extra = 1
    fields = ['trigger', 'effect', 'value', 'condition', 'restriction']

class CardAdmin(admin.ModelAdmin):
    inlines = [CardEffectBindingInline]
    search_fields = ['name']

admin.site.register(Card, CardAdmin)

class DeckCardInline(admin.TabularInline):
    model = DeckCard
    extra = 3
    autocomplete_fields = ['card']

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    inlines = [DeckCardInline]
    list_display = ['name', 'user', 'is_playable_display']
    list_filter = ['user']

    def is_playable_display(self, obj):
        if obj.is_playable():
            return format_html('<span style="color: green;">✔ Playable</span>')
        else:
            issues = obj.get_deck_issues()
            tooltip = " • " + "\n • ".join(issues) if issues else "No details"
            return format_html(
                '<span style="color: red;" title="{}">✖ Not Playable</span>',
                tooltip
            )
    is_playable_display.short_description = 'Playable'
