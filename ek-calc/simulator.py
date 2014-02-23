import random
from copy import deepcopy

import constants
from demons import DemonPlayer


class Fight():
    def __init__(self, player, opp):
        self.player = player
        self.opp = opp
        self.turn = 1
        self.results = list()
        self.dmg_done = 0
        self.dmg_per_min = 0
        self.cooldown = self._calc_cooldown()
        self.player_on_deck = list()
        self.opp_on_deck = list()
        self.player_in_play = list()
        self.opp_in_play = list()
        self.player_turn = False
        self.card = None
        self.def_card = None
        self.index = 0
        self.player_cemetery = list()
        self.opp_cemetery = list()
        self.sim_fight()

    def _calc_cooldown(self):
        deck_cost = 0
        for card in self.player.cards:
            deck_cost += card.cost
        return (60 + 2 * deck_cost)/60

    def sim_fight(self):
        self._prep_cards()
        while self.player.hp > 0 and self.opp.hp > 0:
            self._prep_turn()
            self._handle_runes()
            self._handle_attack()
            self.turn += 1
            self._resolve_all_healths()
        self.fight_summary()

    def fight_summary(self):
        if isinstance(self.opp, DemonPlayer):
            self.dmg_done = self.opp_in_play[0].\
                get_base_hp() - self.opp_in_play[0].hp
            self.dmg_per_min = self.dmg_done / self.cooldown

    def _resolve_all_healths(self):
        for card in self.player_in_play:
            if card.is_dead():
                self.player_in_play.remove(card)
                self.player_cemetery.append(card)
        for card in self.opp_in_play:
            if card.is_dead():
                self.opp_in_play.remove(card)
                self.opp_cemetery.append(card)

    def _damage_adjacent_cards(self, dmg, cards):
        for card in cards:
            card.hp -= dmg

    def _get_adj_cards(self, card):
        adj_cards = list()
        for index in (self.index - 1, self.index, self.index + 1):
            try:
                if card in self.player_in_play:
                    adj_cards.append(self.player_in_play[index])
                else:
                    adj_cards.append(self.opp_in_play[index])
            except IndexError:
                pass
        return adj_cards

    def _get_lowest_hp(self, card):
        lowest_hp_card = card
        if card in self.player_in_play:
            for p_card in self.player_in_play:
                if p_card.hp < lowest_hp_card.hp:
                    lowest_hp_card = p_card
        elif card in self.opp_in_play:
            for o_card in self.opp_in_play:
                if o_card.hp < lowest_hp_card.hp:
                    lowest_hp_card = o_card
        return lowest_hp_card

    def _handle_reflect_summary(self, reflect_summary):
        reflect_damage = 0
        for reflect in reflect_summary:
            dmg = reflect[constants.DAMAGE]
            if reflect[constants.TARGET] == constants.CARD_ACROSS:
                reflect_damage += dmg
            if reflect[constants.TARGET] == constants.CARD_ADJACENT:
                reflect_damage += dmg
                cards = self._get_adj_cards(self.card)
                self._damage_adjacent_cards(dmg, cards)
            if reflect[constants.TARGET] == constants.CARD_LOWEST_HP:
                low_hp_card = self._get_lowest_hp(self.card)
                low_hp_card.hp -= dmg
        return reflect_damage

    def _exile_card(self, card):
        if card in self.player_in_play:
            if hasattr(card, 'resists_exile'):
                return
            card.hp = card.get_base_hp()
            card.effects = dict()
            card.wait = card.starting_wait
            self.player.card_order.append(card)
            self.player_in_play.remove(card)

    def _handle_lowest_hp(self, dmg_summary):
        card = self.def_card
        if card is None:
            if self.player_turn:
                try:
                    card = self._get_lowest_hp(self.player_in_play[0])
                except IndexError:
                    return
            else:
                try:
                    card = self._get_lowest_hp(self.opp_in_play[0])
                except IndexError:
                    return
        low_hp_card = self._get_lowest_hp(card)
        low_hp_card.hp -= dmg_summary[constants.DAMAGE]

    def _handle_conditionals(self, dmg_summary):
        if dmg_summary[constants.TARGET] is constants.CARD_ACROSS:
            if dmg_summary[constants.CONDITION] is constants.CONDITION_TYPE:
                if self.def_card.card_type == \
                        dmg_summary[constants.CONDITION_PARAMETER]:
                    dmg_summary[constants.DAMAGE] = dmg_summary[
                        constants.DAMAGE][1]
                else:
                    dmg_summary[constants.DAMAGE] = dmg_summary[
                        constants.DAMAGE][0]
            reflect_summary = self.def_card.handle_abilities_defense(
                dmg_summary)
            self.card.hp -= self._handle_reflect_summary(reflect_summary)

    def _resolve_damage_through_cards(self, dmg_summary, def_hero):
        if dmg_summary[constants.EFFECT_TYPE] is constants.ATTACK_CONDITIONAL:
            self._handle_conditionals(dmg_summary)
            return
        if dmg_summary[constants.TARGET] is constants.ENEMY_HERO:
            self._direct_damage(dmg_summary, def_hero)
            return
        if dmg_summary[constants.TARGET] is constants.CARD_ACROSS:
            if self.def_card is None or self.def_card.is_dead():
                self._direct_damage(dmg_summary, def_hero)
                return
        if dmg_summary[constants.TARGET] is constants.CARD_LOWEST_HP:
            self._handle_lowest_hp(dmg_summary)
        else:
            if self.def_card is None:
                self._direct_damage(dmg_summary, def_hero)
                return
            if dmg_summary[constants.EFFECT_TYPE] is constants.EXILE:
                self._exile_card(self.def_card)
                self.def_card = None
                return

            reflect_summary = self.def_card.handle_abilities_defense(
                dmg_summary)
            self.card.hp -= self._handle_reflect_summary(reflect_summary)

    def _direct_damage(self, dmg_summary, def_hero):
        dmg_done = 0
        if isinstance(dmg_summary, dict):
            if dmg_summary[constants.EFFECT_TYPE] is \
                    constants.ATTACK_CONDITIONAL:
                dmg_summary[constants.DAMAGE] = dmg_summary[
                    constants.DAMAGE][0]
            if dmg_summary[constants.TARGET] in \
                    (constants.ENEMY_HERO, constants.CARD_ACROSS):
                dmg_done += dmg_summary[constants.DAMAGE]
        elif isinstance(dmg_summary, (list, tuple)):
            for dmg in dmg_summary:
                if dmg[constants.EFFECT_TYPE] is constants.ATTACK_CONDITIONAL:
                    dmg[constants.DAMAGE] = dmg[constants.DAMAGE][0]
                if dmg[constants.TARGET] in \
                        (constants.ENEMY_HERO, constants.CARD_ACROSS):
                    dmg_done += dmg[constants.DAMAGE]
        def_hero.hp -= dmg_done

    def _handle_attack(self):
        if self.player_turn:
            for index, card in enumerate(self.player_in_play):
                self.index = index
                self.card = card
                self._attack_with_card(self.opp, self.opp_in_play)
            self.player_turn = False
        else:
            for index, card in enumerate(self.opp_in_play):
                self.index = index
                self.card = card
                self._attack_with_card(self.player, self.player_in_play)
            self.player_turn = True

    def _is_in_play(self, card):
        for in_play in (self.player_in_play, self.opp_in_play):
            if card in in_play:
                return True
        return False

    def _damage_through_cards(self, dmg_summary, def_hero):
        for dmg in dmg_summary:
            if self.card.is_dead():
                break
            self._resolve_damage_through_cards(dmg, def_hero)

    def _attack_with_card(self, opp, opp_in_play):
        dmg_summary = self.card.handle_abilities_offense()
        if len(opp_in_play) <= self.index:
            self._direct_damage(dmg_summary, opp)
        elif len(opp_in_play) > self.index:
            self.def_card = opp_in_play[self.index]
            self._damage_through_cards(dmg_summary, opp)

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
                    self.player_in_play.append(card)
            for card in self.player_in_play:
                if card in self.player_on_deck:
                    self.player_on_deck.remove(card)
        else:
            for card in self.opp_on_deck:
                if card.wait == 0:
                    self.opp_in_play.append(card)
            for card in self.opp_in_play:
                if card in self.opp_on_deck:
                    self.opp_on_deck.remove(card)

    def _reduce_wait(self):
        for card in self.player_on_deck:
            card.wait -= 1
        for card in self.opp_on_deck:
            card.wait -= 1

    def _put_cards_on_deck(self):
        if self.player_turn:
            if len(self.player.card_order) > 0:
                self.player_on_deck.append(self.player.card_order[0])
                self.player.card_order.pop(0)
        else:
            if len(self.opp.card_order) > 0:
                self.opp_on_deck.append(self.opp.card_order[0])
                self.opp.card_order.pop(0)

    def _prep_cards(self):
        cards_to_order = deepcopy(self.player.cards)
        while len(self.player.card_order) != len(self.player.cards):
            random_index = random.choice(range(0, len(cards_to_order)))
            self.player.card_order.append(cards_to_order[random_index])
            cards_to_order.pop(random_index)

        cards_to_order = deepcopy(self.opp.cards)
        while len(self.opp.card_order) != len(self.opp.cards):
            random_index = random.choice(range(0, len(cards_to_order)))
            self.opp.card_order.append(cards_to_order[random_index])
            cards_to_order.pop(random_index)
