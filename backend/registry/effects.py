
def apply_haste(card):
    print(f"{card.name} gains Haste!")

def draw_card(card):
    print(f"Drawing a card because of {card.name}'s ability.")

    '''
    
    player = card.owner
    deck = player.deck

    if deck.cards.exists():
        drawn_card = deck.cards.first()
        player.hand.add(drawn_card)
        deck.cards.remove(drawn_card)
        print(f"{player.username} draws {drawn_card.name}")
    else:
        print("Deck is empty!")

    '''

EFFECT_REGISTRY = {
    "haste": apply_haste,
    "draw_card": draw_card,
}
