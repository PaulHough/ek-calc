#! /usr/bin/env python3
import itertools
import sys
import random
from copy import copy
from datetime import datetime

from player import Player
from simulator import Fight
import demons
from my_cards import player_deck, player_runes, PLAYER_LVL, DEMON_CARD


def get_possible_decks():
    decks = list([])
    deck_without_forced_cards = list([])
    deck_with_forced_cards = list([])

    for card in player_deck:
        if len(card) >= 4:
            card_is_forced = card[3]
            if card_is_forced:
                random_index = random.randrange(0, len(deck_with_forced_cards) + 1)
                deck_with_forced_cards.insert(random_index, card)
            else:
                random_index = random.randrange(0, len(deck_without_forced_cards) + 1)
                deck_without_forced_cards.insert(random_index, card)
        else:
            random_index = random.randrange(0, len(deck_without_forced_cards) + 1)
            deck_without_forced_cards.insert(random_index, card)

    for r in range(1, len(deck_without_forced_cards) + 1):
        if (r + len(deck_with_forced_cards)) > \
                Player(PLAYER_LVL).get_num_of_cards_allowed():
            continue
        decks.extend(list(itertools.combinations(deck_without_forced_cards, r=r)))

    decks = [list(deck) for deck in decks]

    for forced_card in deck_with_forced_cards:
        for deck in decks:
            random_index = random.randrange(0, len(deck) + 1)
            deck.insert(random_index, forced_card)

    if len(decks) < 1 and len(deck_with_forced_cards) > 0:
        decks.append(deck_with_forced_cards)
    
    return decks


def get_possible_runes():
    runes = list([])
    for r in range(1, len(player_runes) + 1):
        if r > Player(PLAYER_LVL).get_num_of_runes_allowed():
            continue
        runes.extend(list(itertools.permutations(player_runes, r=r)))
    return runes


def handle_reports(reports):
    best_report = copy(reports[0])
    for report in reports:
        if report['dpm'] > best_report['dpm']:
            best_report = copy(report)
    print('\nBest Deck for {}: '.format(DEMON_CARD))
    for i, card in enumerate(best_report['deck']):
        print('\t{}. {}'.format(i + 1, card))
    print('Rune Order: ')
    if best_report['runes'] is not None:
        for i, rune in enumerate(best_report['runes']):
            print('\t{}. {}'.format(i + 1, rune))
    print('\nMaximum Damage Per Minute: {:.0f}'.format(best_report['dpm']))
    print('Average Damage Done Per Fight: {:.0f}'.format(best_report['avg_dmg']))
    print('Average Rounds Lasted Per Fight: {:.0f}'.format(best_report['avg_rounds']))


def create_new_players(deck, runes):
    player = Player(PLAYER_LVL)

    # new_card = (card, level, is_merit)
    for new_card in deck:
        card = new_card[0]
        lvl = new_card[1]
        is_merit = False
        if len(new_card) >= 3:
            is_merit = new_card[2]

        player.assign_card(card(lvl, is_merit))

    demon_player = demons.DemonPlayer()
    demon_player.assign_card(DEMON_CARD())

    if runes is None:
        return player, demon_player
    for rune, lvl in runes:
        player.assign_rune(rune(lvl))
    return player, demon_player


def run_simulation_with_decks(decks, reports, fight_count, runes=None):
    for deck in decks:
        damage_done = 0
        damage_per_minute = 0
        rounds_lasted = 0
        for _ in itertools.repeat(None, fight_count):
            player, demon_player = create_new_players(deck, runes)
            fight = Fight(player, demon_player)
            damage_done += fight.damage_done
            damage_per_minute += fight.damage_per_minute
            rounds_lasted += fight.current_turn
        reports.append({
            'dpm': damage_per_minute / fight_count,
            'avg_dmg': damage_done / fight_count,
            'avg_rounds': rounds_lasted / fight_count,
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
    damage_done = 0
    damage_per_minute = 0
    for _ in itertools.repeat(None, cnt):
        player, demon_player = create_new_players(player_deck, player_runes)
        fight = Fight(player, demon_player)
        damage_done += fight.damage_done
        damage_per_minute += fight.damage_per_minute
    print('Average Damage Per Minute: {:.0f}'.format(damage_per_minute / cnt))


if __name__ == '__main__':
    simulation_start_time = datetime.now()
    if len(sys.argv) == 3:
        try:
            fight_count_per_deck = int(sys.argv[2])
        except ValueError:
            err_msg = 'Expected an integer value. Received {} instead.' \
                ' Please provide an integer value representing the number of' \
                ' fights per deck you wish to simulate.'.format(
                    type(sys.argv[1]))
            raise TypeError(err_msg)
        handle_single_deck_simulation(fight_count_per_deck)
    elif len(sys.argv) < 3:
        if len(sys.argv) == 2:
            try:
                fight_count_per_deck = int(sys.argv[1])
            except ValueError:
                err_msg = 'Expected an integer value. Received {} instead. ' \
                    'Please provide an integer value representing the number' \
                    ' of fights per deck you wish to simulate.'.format(
                        type(sys.argv[1]))
                raise TypeError(err_msg)
        else:
            fight_count_per_deck = 1
        handle_simulations(fight_count_per_deck)

    simulation_end_time = datetime.now()
    simulation_total_time = simulation_end_time - simulation_start_time
    print('Simulation took: {}\n'.format(simulation_total_time))
