from django import forms
from django.contrib import admin
from django.utils.html import format_html
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
    CharacterRelationship,
    Faction,
    Subtype,
)

from backend.registry.character_abilities import CHARACTER_ABILITY_METADATA
from backend.registry.deck_restrictions import DECK_RESTRICTION_REGISTRY
from backend.registry.partner_abilities import PARTNER_ABILITY_REGISTRY
from backend.registry.solo_abilities import SOLO_BONUS_REGISTRY


### ---- Character Admin Form ----

class CharacterAdminForm(forms.ModelForm):
    def _get_filtered_choices(ability_type):
        return [("", "— None —")] + [
            (name, name)
            for name, meta in CHARACTER_ABILITY_METADATA.items()
            if meta["type"] == ability_type
        ]

    def _get_deck_restriction_choices():
        return [("", "— None —")] + [
            (name, name) for name in DECK_RESTRICTION_REGISTRY.keys()
        ]

    def _get_partner_ability_choices():
        return [("", "— None —")] + [
            (name, name) for name in PARTNER_ABILITY_REGISTRY.keys()
        ]

    def _get_solo_bonus_choices():
        return [("", "— None —")] + [
            (name, name) for name in SOLO_BONUS_REGISTRY.keys()
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

    partner_ability_ref = forms.ChoiceField(
        choices=_get_partner_ability_choices(),
        required=False,
        label="Partner Ability"
    )

    solo_bonus_ref = forms.ChoiceField(
        choices=_get_solo_bonus_choices(),
        required=False,
        label="Solo Bonus"
    )

    deck_restriction_ref = forms.ChoiceField(
        choices=_get_deck_restriction_choices(),
        required=False,
        label="Deck Restriction"
    )

    class Meta:
        model = Character
        fields = "__all__"


### ---- Character Admin ----

class CharacterAdmin(admin.ModelAdmin):
    form = CharacterAdminForm
    list_display = ['name', 'class_type', 'faction']
    list_filter = ['class_type', 'faction']
    search_fields = ['name']
    filter_horizontal = ['subtypes']


### ---- Register Models ----

admin.site.register(Character, CharacterAdmin)
admin.site.register(Faction)
admin.site.register(Subtype)
admin.site.register(Effect)
admin.site.register(Condition)
admin.site.register(Restriction)
admin.site.register(CardEffectBinding)
admin.site.register(CharacterRelationship)


### ---- Trigger Admin ----

@admin.register(Trigger)
class TriggerAdmin(admin.ModelAdmin):
    list_display = ['script_reference', 'description', 'zone']
    list_filter = ['zone']


### ---- Card Admin ----

class CardEffectBindingInline(admin.TabularInline):
    model = CardEffectBinding
    extra = 1
    fields = ['trigger', 'effect', 'value', 'condition', 'restriction']


class CardAdmin(admin.ModelAdmin):
    inlines = [CardEffectBindingInline]
    search_fields = ['name']
    filter_horizontal = ['subtypes']

admin.site.register(Card, CardAdmin)


### ---- Deck Admin ----

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
