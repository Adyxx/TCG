import os
import sys
import django


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend_web')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frontend_web.frontend_web.settings')

django.setup()

from backend.models import Card, Trigger, Effect, Condition, Restriction, CardEffectBinding, User
from backend.registry.effects import EFFECT_REGISTRY
from backend.registry.conditions import CONDITION_REGISTRY
from backend.registry.restrictions import RESTRICTION_REGISTRY, reset_restriction_state


class MockPlayer:
    def __init__(self, username, health=20, cards_played_this_turn=0):
        self.username = username
        self.health = health
        self.cards_played_this_turn = cards_played_this_turn

    def __str__(self):
        return self.username


def execute_trigger(card, trigger_code):
    print(f"\nTriggering: {trigger_code} on card {card.name}")

    for binding in card.effect_bindings.filter(trigger__code=trigger_code):
        print(f"→ Checking binding: {binding}")

        if binding.restriction:
            restriction_func = RESTRICTION_REGISTRY.get(binding.restriction.code)
            if restriction_func:
                allowed = restriction_func(card, binding.id)
                if not allowed:
                    print("🚫 Restriction blocked this effect.")
                    continue

        if binding.condition:
            condition_func = CONDITION_REGISTRY.get(binding.condition.script_reference)
            if condition_func and not condition_func(card):
                print("🟡 Condition not met.")
                continue

        effect_func = EFFECT_REGISTRY.get(binding.effect.script_reference)
        if effect_func:
            print("✅ Executing effect...")
            effect_func(card)
        else:
            print("❌ Effect function not found.")


def run_test():
    reset_restriction_state()

    cards = Card.objects.all()

    if not cards.exists():
        print("❌ No cards found. Please create some in admin.")
        return

    triggers_to_test = ["on_play", "on_draw", "on_turn_start", "self_hurt_2"]

    for idx, card in enumerate(cards, start=1):
        print(f"\n=== 🃏 Testing Card {idx}: {card.name} ===")

        mock_player = MockPlayer(f"Player{idx}", health=15 + idx, cards_played_this_turn=idx % 3)
        card.owner = mock_player

        for trigger_code in triggers_to_test:
            execute_trigger(card, trigger_code)


if __name__ == "__main__":
    run_test()
