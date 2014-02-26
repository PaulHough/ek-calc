#! /usr/bin/env python3
import itertools
import sys
from copy import deepcopy
from datetime import datetime

from player import Player
from simulator import Fight
import demons
from my_cards import player_deck, player_runes

DEBUG = False
PLAYER_LVL = 50
DEMON_CARD = demons.DarkTitan()


def get_possible_decks():
    decks = list([])
    for r in range(1, len(player_deck) + 1):
        if r > Player(PLAYER_LVL).get_num_of_cards_allowed():
            continue
        decks.extend(list(itertools.combinations(player_deck, r=r)))
    return decks


def get_possible_runes():
    runes = list([])
    for r in range(1, len(player_runes) + 1):
        if r > Player(PLAYER_LVL).get_num_of_runes_allowed():
            continue
        for possible_list in itertools.permutations(player_runes, r=r):
            should_add = True
            for rune in possible_list:
                for other_rune in possible_list:
                    if rune == other_rune:
                        continue
                    if rune.name == other_rune.name:
                        should_add = False
            if should_add:
                runes.append(list(possible_list))
    return runes


def handle_reports(reports):
    max_dpm = 0
    best_report = dict()
    for report in reports:
        if report['dpm'] > max_dpm:
            max_dpm = report['dpm']
            best_report = deepcopy(report)
    print('Best Deck: ')
    for i, card in enumerate(best_report['deck']):
        print('\t{}. {}'.format(i + 1, card))
    print('Rune Order: ')
    for i, rune in enumerate(best_report['runes']):
        print('\t{}. {}'.format(i + 1, rune))
    print('Max Damage Per Minute: {:.0f}'.format(best_report['dpm']))
    print('Average Damage Done: {:.0f}'.format(best_report['avg_dmg']))


def create_new_players(deck, runes):
    player = Player(PLAYER_LVL)
    for card in deck:
        player.assign_card(card)
    for rune in runes:
        player.assign_rune(rune)
    demon_player = demons.DemonPlayer()
    demon_player.assign_card(DEMON_CARD)
    return player, demon_player


def handle_simulations(cnt=1):
    decks = get_possible_decks()
    runes_set = get_possible_runes()
    reports = list()
    print('Calculated {} possible deck and rune combinations'.format(
        len(decks) * len(runes_set)))
    for runes in runes_set:
        for deck in decks:
            dmg_done = 0
            dmg_per_min = 0
            i = 1
            for _ in itertools.repeat(None, cnt):
                print('Running Simulation {} of {}'.format(i, cnt))
                player, demon_player = create_new_players(deck, runes)
                fight = Fight(player, demon_player)
                dmg_done += fight.dmg_done
                dmg_per_min += fight.dmg_per_min
            reports.append({
                'dpm': dmg_per_min / cnt,
                'avg_dmg': dmg_done/cnt,
                'deck': deck,
                'runes': runes
            })
    handle_reports(reports)


def handle_single_deck_simulation(cnt=1):
    dmg_done = 0
    dmg_per_min = 0
    for _ in itertools.repeat(None, cnt):
        player, demon_player = create_new_players(player_deck, player_runes)
        fight = Fight(player, demon_player)
        dmg_done += fight.dmg_done
        dmg_per_min += fight.dmg_per_min
    print('Average Damage Per Minute: {:.0f}'.format(dmg_per_min/cnt))


if __name__ == '__main__':
    start = datetime.now()
    if len(sys.argv) == 3:
        try:
            count = int(sys.argv[2])
        except ValueError:
            err_msg = 'Expected integer received {} instead'.format(
                type(sys.argv[1]))
            raise TypeError(err_msg)
        handle_single_deck_simulation(count)
    elif len(sys.argv) < 3:
        if len(sys.argv) == 2:
            try:
                count = int(sys.argv[1])
            except ValueError:
                err_msg = 'Expected integer received {} instead'.format(
                    type(sys.argv[1]))
                raise TypeError(err_msg)
        else:
            count = 1
        handle_simulations(count)
    print('Simulation took: {}'.format(datetime.now() - start))
