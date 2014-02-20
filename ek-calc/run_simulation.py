#! /usr/bin/env python3
import itertools

from player import Player
from simulator import Fight
import demons
import cards


def handle_simulation():
    player = Player(28)
    card = cards.HeadlessHorseman(5)
    for _ in itertools.repeat(None, 3):
        player.assign_card(card)

    demon = demons.DarkTitan()
    demon_player = demons.DemonPlayer()
    demon_player.assign_card(demon)
    fight = Fight(player, demon_player)
    print(fight.results)

if __name__ == '__main__':
    handle_simulation()
