import random
from copy import deepcopy

import constants


class Fight():
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 1
        self.results = list()
        self.turn_results = list()
        self.player_on_deck = list()
        self.enemy_on_deck = list()
        self.player_in_play = list()
        self.enemy_in_play = list()
        self.player_turn = False
        self.dmg_done = 0
        self.dmg_per_min = 0
        self.cooldown = self._calc_cooldown()
        self.sim_fight()

    def _calc_cooldown(self):
        deck_cost = 0
        for card in self.player.cards:
            deck_cost += card.cost
        return (60 + 2 * deck_cost)/60

    def sim_fight(self):
        self._prep_cards()
        while self.player.hp > 0 and self.enemy.hp > 0:
            self.turn_results = [
                '{}\n{} Turn: {}'.format(
                    '-'*40, 'Player' if self.player_turn else 'Enemy',
                    self.turn),
                'Player HP: {}\nEnemy HP: {}'.format(
                    self.player.hp, self.enemy.hp),
                '\nPlayer Cards in Play: {}'.format(self.player_in_play),
                'Enemy Cards in Play: {}'.format(self.enemy_in_play),
            ]
            self._prep_turn()

            self.turn_results.extend([
                '\nPlayer Cards on Deck: {}'.format(self.player_on_deck),
                'Enemy Cards on Deck: {}'.format(self.enemy_on_deck)
            ])

            self._handle_runes()
            self._handle_attack()
            self.turn += 1
            self._resolve_all_healths()

            self.turn_results.extend(['\n\n'])
            self.results.append(self.turn_results)

        self.fight_summary()

    def fight_summary(self):
        winner = self.enemy
        if self.enemy.hp < self.player.hp:
            winner = self.player
        self.dmg_done = self.enemy_in_play[0]._get_base_hp() - \
                        self.enemy_in_play[0].hp
        self.dmg_per_min = self.dmg_done / self.cooldown
        self.results.append([
            'Winner: {}'.format(winner),
            'Total Damage to Card: {}'.format(self.dmg_done),
            '\n\n'
        ])

    def _handle_attack(self):
        if self.player_turn:
            for i, card in enumerate(self.player_in_play):
                self._player_attack_with_card(i, card)
            self.player_turn = False
        else:
            for i, card in enumerate(self.enemy_in_play):
                self._enemy_attack_with_card(i, card)
            self.player_turn = True

    def _resolve_all_healths(self):
        for card in self.player_in_play:
            if card.is_dead():
                self.player_in_play.remove(card)
        for card in self.enemy_in_play:
            if card.is_dead():
                self.enemy_in_play.remove(card)

    def _resolve_damage_through_cards(
            self, atk_card, def_card, dmg_summary, def_hero):
            if atk_card.is_dead():
                self. turn_results.extend(
                    ['{} Was Killed in Battle'.format(atk_card)])
            else:
                if dmg_summary[constants.EFFECT_TYPE] is constants.ENEMY_HERO:
                    def_hero.hp -= dmg_summary[constants.DAMAGE]
                    self.turn_results.extend(
                        ['{} Took {} Damage'.format(
                            def_hero, dmg_summary[constants.DAMAGE])])
                    return
                if def_card.is_dead() and \
                        dmg_summary[constants.EFFECT_TYPE] is constants.ATTACK:
                    def_hero.hp -= dmg_summary[constants.DAMAGE]
                    self.turn_results.extend(
                        ['{} Took {} Damage'.format(
                            def_hero, dmg_summary[constants.DAMAGE])])
                else:
                    pre_hp = def_card.hp
                    atk_card.hp -= def_card.handle_abilities_defense(
                        dmg_summary)
                    post_hp = def_card.hp
                    self.turn_results.extend(
                        ['{} Took {} Defending'.format(
                            def_card, pre_hp - post_hp)])
                    if def_card.is_dead():
                        self.turn_results.extend(
                            ['{} Was Killed in Battle'.format(def_card)])

    def _damage_through_cards(
            self, dmg_summary, atk_card, def_card, def_hero):
        if isinstance(dmg_summary, (list, tuple)):
            for dmg in dmg_summary:
                if atk_card.is_dead():
                    self. turn_results.extend(
                        ['{} Was Killed in Battle'.format(atk_card)])
                    break
                self._resolve_damage_through_cards(
                    atk_card, def_card, dmg, def_hero)
        elif isinstance(dmg_summary, dict):
            self._resolve_damage_through_cards(
                atk_card, def_card, dmg_summary, def_hero)

    def _direct_damage(self, dmg_summary, def_hero):
        dmg_to_enemy = 0
        if isinstance(dmg_summary, (list, tuple)):
            for dmg in dmg_summary:
                if dmg[constants.EFFECT_TYPE] in \
                        constants.DAMAGE_TO_HERO_EFFECT_TYPES:
                    dmg_to_enemy += dmg[constants.DAMAGE]
        elif isinstance(dmg_summary, dict):
            if dmg_summary[constants.EFFECT_TYPE] in \
                    constants.DAMAGE_TO_HERO_EFFECT_TYPES:
                dmg_to_enemy = dmg_summary[constants.DAMAGE]
        def_hero.hp -= dmg_to_enemy
        self.turn_results.extend(['Enemy Took {} Damage'.format(dmg_to_enemy)])

    def _player_attack_with_card(self, i, card):
        self.turn_results.extend(['\nCard Attacking: {}'.format(card)])
        dmg_summary = card.handle_abilities_offense()
        self.turn_results.extend(['Damage Summary: {}'.format(dmg_summary)])
        if len(self.enemy_in_play) <= i:
            self._direct_damage(dmg_summary, self.enemy)
        elif len(self.enemy_in_play) > i:
            self._damage_through_cards(
                dmg_summary, card, self.enemy_in_play[i], self.enemy)

    def _enemy_attack_with_card(self, i, card):
        self.turn_results.extend(['Card Attacking: {}'.format(card)])
        dmg_summary = card.handle_abilities_offense()
        self.turn_results.extend(['Damage Summary: {}'.format(dmg_summary)])
        if len(self.player_in_play) == 0:
            self._direct_damage(dmg_summary, self.player)
        elif len(self.player_in_play) > i:
            self._damage_through_cards(
                dmg_summary, card, self.player_in_play[i], self.player)

    def _handle_runes(self):
        pass

    def _prep_turn(self):
        self._put_cards_in_play()
        self._put_cards_on_deck()

    def _put_cards_in_play(self):
        self._reduce_wait()
        if self.player_turn:
            for card in self.player_on_deck:
                if card.wait == 0:
                    self.turn_results.extend(
                        ['Card Going Into Play: {}'.format(card)])
                    self.player_in_play.append(card)
            for card in self.player_in_play:
                if card in self.player_on_deck:
                    self.player_on_deck.remove(card)
        else:
            for card in self.enemy_on_deck:
                if card.wait == 0:
                    self.turn_results.extend(
                        ['Card Going Into Play: {}'.format(card)])
                    self.enemy_in_play.append(card)
            for card in self.enemy_in_play:
                if card in self.enemy_on_deck:
                    self.enemy_on_deck.remove(card)

    def _reduce_wait(self):
        for card in self.player_on_deck:
            card.wait -= 1
        for card in self.enemy_on_deck:
            card.wait -= 1

    def _put_cards_on_deck(self):
        if self.player_turn:
            if len(self.player.card_order) > 0:
                self.player_on_deck.append(self.player.card_order[0])
                self.player.card_order.pop(0)
        else:
            if len(self.enemy.card_order) > 0:
                self.enemy_on_deck.append(self.enemy.card_order[0])
                self.enemy.card_order.pop(0)

    def _prep_cards(self):
        cards_to_order = deepcopy(self.player.cards)
        while len(self.player.card_order) != len(self.player.cards):
            random_index = random.choice(range(0, len(cards_to_order)))
            self.player.card_order.append(cards_to_order[random_index])
            cards_to_order.pop(random_index)

        cards_to_order = deepcopy(self.enemy.cards)
        while len(self.enemy.card_order) != len(self.enemy.cards):
            random_index = random.choice(range(0, len(cards_to_order)))
            self.enemy.card_order.append(cards_to_order[random_index])
            cards_to_order.pop(random_index)
