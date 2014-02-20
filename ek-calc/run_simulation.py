#! /usr/bin/env python3
import itertools

from player import Player
from simulator import Fight
import demons
import cards


def handle_simulation():
    player = Player(28)
    for _ in itertools.repeat(None, 3):
        player.assign_card(cards.HeadlessHorseman(5))

    demon_player = demons.DemonPlayer()
    demon_player.assign_card(demons.DarkTitan())
    fight = Fight(player, demon_player)

    for turn in fight.results:
        for j in turn:
            print(j)
            continue

if __name__ == '__main__':
    handle_simulation()
