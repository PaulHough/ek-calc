import cards
import runes


player_deck = (
    cards.HeadlessHorseman(10),
    cards.HeadlessHorseman(10),
    cards.HeadlessHorseman(10),
    cards.HeadlessHorseman(10),
    cards.WoodElfArcher(10),
    cards.WoodElfArcher(10),
    cards.WoodElfArcher(10),
)

player_runes = (
    runes.Revival(4),
)

try:
    from my_cards_local import *
except ImportError:
    pass
