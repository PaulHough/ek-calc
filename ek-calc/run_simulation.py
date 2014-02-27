#! /usr/bin/env python3
import itertools
import sys
from copy import deepcopy
from datetime import datetime

from player import Player
from simulator import Fight
import demons
from my_cards import player_deck, player_runes, PLAYER_LVL, DEMON_CARD


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
        runes.extend(list(itertools.permutations(player_runes, r=r)))
    return runes


def handle_reports(reports):
    best_report = deepcopy(reports[0])
    for report in reports:
        if report['dpm'] > best_report['dpm']:
            best_report = deepcopy(report)
    print('\nBest Deck for {}: '.format(DEMON_CARD))
    for i, card in enumerate(best_report['deck']):
        print('\t{}. {}'.format(i + 1, card))
    print('Rune Order: ')
    if best_report['runes'] is not None:
        for i, rune in enumerate(best_report['runes']):
            print('\t{}. {}'.format(i + 1, rune))
    print('\nMax Damage Per Minute: {:.0f}'.format(best_report['dpm']))
    print('Average Damage Done: {:.0f}'.format(best_report['avg_dmg']))
    print('Average Rounds Lasted: {:.0f}'.format(best_report['avg_rounds']))


def create_new_players(deck, runes):
    player = Player(PLAYER_LVL)
    for val in deck:
        merit = False
        if len(val) == 3:
            merit = val[2]
        card = val[0]
        lvl = val[1]
        player.assign_card(card(lvl, merit))
    demon_player = demons.DemonPlayer()
    demon_player.assign_card(DEMON_CARD())

    if runes is None:
        return player, demon_player
    for rune, lvl in runes:
        player.assign_rune(rune(lvl))
    return player, demon_player


def run_simulation_with_decks(decks, reports, cnt, runes=None):
    for deck in decks:
        dmg_done = 0
        dmg_per_min = 0
        rounds_lasted = 0
        for _ in itertools.repeat(None, cnt):
            player, demon_player = create_new_players(deck, runes)
            fight = Fight(player, demon_player)
            dmg_done += fight.dmg_done
            dmg_per_min += fight.dmg_per_min
            rounds_lasted += fight.turn
        reports.append({
            'dpm': dmg_per_min / cnt,
            'avg_dmg': dmg_done/cnt,
            'avg_rounds': rounds_lasted/cnt,
            'deck': deck,
            'runes': runes
        })


def handle_simulations(cnt=1):
    decks = get_possible_decks()
    runes_set = get_possible_runes()
    reports = list()
    combinations = len(decks) * len(runes_set)
    if len(runes_set) == 0:
        combinations = len(decks)
    print('Calculated {} possible deck and rune combinations'.format(
        combinations))
    print('Running {} simulations.'.format(combinations * cnt))
    if len(runes_set) == 0:
        run_simulation_with_decks(decks, reports, cnt)
    for runes in runes_set:
        print('Simulating for runes:')
        for rune in runes:
            print('\t{}'.format(rune))
        run_simulation_with_decks(decks, reports, cnt, runes)
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
    print('Simulation took: {}\n'.format(datetime.now() - start))
