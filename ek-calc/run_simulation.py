#! /usr/bin/env python3
import itertools
import sys

from player import Player
from simulator import Fight
import demons
import cards

DEBUG = False


def multiple_simulations(cnt=1):
    dmg_done = 0
    dmg_per_min = 0
    for _ in itertools.repeat(None, cnt):
        fight = handle_simulation()
        dmg_done += fight.dmg_done
        dmg_per_min += fight.dmg_per_min

        if DEBUG:
            for turn in fight.results:
                for j in turn:
                    print(j)
                    continue

    avg_dmg = dmg_done/count
    avg_dmg_per_min = dmg_per_min / count
    print('Average Damage Done: {}'.format(int(avg_dmg)))
    print('Damage Per Minute: {:.2f}'.format(int(avg_dmg_per_min)))


def handle_simulation():
    player_level = 30
    player = Player(player_level)
    player.assign_card(cards.HeadlessHorseman(10))
    player.assign_card(cards.HeadlessHorseman(8))
    player.assign_card(cards.HeadlessHorseman(5))

    demon_player = demons.DemonPlayer()
    demon_player.assign_card(demons.DarkTitan())
    return Fight(player, demon_player)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        try:
            count = int(sys.argv[1])
        except ValueError:
            err_msg = 'Expected integer received {} instead'.format(
                type(sys.argv[1]))
            raise TypeError(err_msg)
    elif len(sys.argv) == 1:
        count = 1
    else:
        err_msg = 'run_simulation takes 1 positional argument but {} were ' \
                  'given'.format(len(sys.argv) - 1)
        raise TypeError(err_msg)
    multiple_simulations(count)
