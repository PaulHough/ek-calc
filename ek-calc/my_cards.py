import cards
import runes
import demons

PLAYER_LVL = 25
DEMON_CARD = demons.SeaKing

## Format = (cards.CARDNAME, CARDLEVEL (0-10), [Optional] True/False - Whether the card is a merit card or not)
## Example: (cards.WoodElfArcher, 10, True),

player_deck = (
    (cards.HeadlessHorseman, 10),
    (cards.HeadlessHorseman, 10),
    (cards.HeadlessHorseman, 10),
    (cards.WoodElfArcher, 10, True),
    (cards.WoodElfArcher, 10, True),
    (cards.WoodElfArcher, 10, True),
)

player_runes = (
    (runes.Revival, 4),
    (runes.Leaf, 4),
)

try:
    from my_cards_local import *
except ImportError:
    pass
