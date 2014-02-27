import cards
import runes
import demons

PLAYER_LVL = 25
DEMON_CARD = demons.SeaKing

player_deck = (
    (cards.HeadlessHorseman, 10),
    (cards.HeadlessHorseman, 10),
    (cards.HeadlessHorseman, 10),
    (cards.WoodElfArcher, 10),
    (cards.WoodElfArcher, 10),
    (cards.WoodElfArcher, 10),
)

player_runes = (
    (runes.Revival, 4),
    (runes.Leaf, 4),
)

try:
    from my_cards_local import *
except ImportError:
    pass
