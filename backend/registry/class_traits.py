from backend.registry._base import AbilityRegistry

CLASS_TRAITS = AbilityRegistry()

@CLASS_TRAITS.register(
    "KNIGHT",
    type="passive",
    description="Gain +1 temporary energy when a unit dies (max once per turn).",
    trigger="on_friendly_death",
    condition="has_not_triggered_this_turn"
)
def knight_trait(player):
    player.energy += 1

@CLASS_TRAITS.register(
    "WIZARD",
    type="passive",
    description="Discard a card to gain +1 temporary energy.",
    trigger="on_discard",
    condition="has_not_triggered_this_turn"
)

def wizard_trait(player):
    player.energy += 1
