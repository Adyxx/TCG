from django import forms
from django.contrib import admin
from django.utils.html import format_html, format_html_join
from django.db import models 

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
    CharacterPairSynergy,
    CharacterRelationship,
)

from backend.registry.character_abilities import CHARACTER_ABILITY_METADATA

class CharacterAdminForm(forms.ModelForm):
    def _get_filtered_choices(ability_type):
        return [("", "— None —")] + [
            (name, name)
            for name, meta in CHARACTER_ABILITY_METADATA.items()
            if meta["type"] == ability_type
        ]

    passive_ability_ref = forms.ChoiceField(
        choices=_get_filtered_choices("passive"),
        required=False,
        label="Passive Ability"
    )

    active_ability_ref = forms.ChoiceField(
        choices=_get_filtered_choices("active"),
        required=False,
        label="Active Ability"
    )

    class Meta:
        model = Character
        fields = "__all__"

class CharacterAdmin(admin.ModelAdmin):
    form = CharacterAdminForm


admin.site.register(Character, CharacterAdmin)
admin.site.register(Effect)
admin.site.register(Condition)
admin.site.register(Restriction)
admin.site.register(CardEffectBinding)
admin.site.register(CharacterPairSynergy)
admin.site.register(CharacterRelationship)

@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ['script_reference', 'description', 'zone']
    list_filter = ['zone']

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
