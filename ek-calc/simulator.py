import random
from copy import deepcopy, copy

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

    def sim_fight(self):
        self._prep_cards()
        while self.player.hp > 0 and self.opp.hp > 0 and \
                (len(self.player.card_order) > 0 or
                 len(self.player_on_deck) > 0 or
                 len(self.player_in_play) > 0):
            self._prep_turn()
            self._handle_runes()
            self._resolve_all_healths()
            self._handle_attack()
            self._resolve_all_healths()
            self.turn += 1
        self.fight_summary()

    def _calc_cooldown(self):
        deck_cost = 0
        for card in self.player.cards:
            deck_cost += card.cost
        return (60 + 2 * deck_cost)/60

    def fight_summary(self):
        if isinstance(self.opp, DemonPlayer):
            self.dmg_done = self.opp_in_play[0].\
                get_base_hp() - self.opp_in_play[0].hp
            for card in self.player.cards:
                if card.merit:
                    self.dmg_done += 100
            self.dmg_per_min = self.dmg_done / self.cooldown

    def _handle_exiting_effects(self, card):
        exit_summary = card.exit_effect()
        for effect in exit_summary:
            self._handle_effect(effect)

    def _put_card_in_cemetery_from_deck(self, card):
        if card in self.player_on_deck:
            self.player_on_deck.remove(card)
            if card.should_res:
                self.player.card_order.append(card)
                return
            self.player_cemetery.append(card)
        else:
            self.opp_on_deck.remove(card)
            if card.should_res:
                self.opp.card_order.append(card)
                return
            self.opp_cemetery.append(card)

    def _put_card_in_cemetery_from_play(self, card):
        if card is self.def_card:
            self.def_card = None
        if card in self.player_in_play:
            self.player_in_play.remove(card)
            if card.should_res:
                self.player.card_order.append(card)
                self._handle_exiting_effects(card)
                return
            self.player_cemetery.append(card)
            self._handle_exiting_effects(card)
        else:
            self.opp_in_play.remove(card)
            if card.should_res:
                self.opp.card_order.append(card)
                self._handle_exiting_effects(card)
                return
            self.opp_cemetery.append(card)
            self._handle_exiting_effects(card)

    def _resolve_all_healths(self):
        for card in self.player_in_play:
            if card.is_dead():
                self._put_card_in_cemetery_from_play(card)
        for card in self.opp_in_play:
            if card.is_dead():
                self._put_card_in_cemetery_from_play(card)

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

    def _destroy_card(self, card):
        if card in self.player_in_play:
            if card.resists_destroy():
                return
            self._put_card_in_cemetery_from_play(card)

    def _exile_card(self, card):
        if card in self.player_in_play:
            if card.resists_exile():
                return
            self.player.card_order.append(card)
            self.player_in_play.remove(card)
            self._handle_exiting_effects(card)

    def _handle_lowest_hp_for_dmg(self, dmg_summary):
        card = self.def_card
        if card is None:
            if self.player_turn:
                try:
                    card = self._get_lowest_hp(self.opp_in_play[0])
                except IndexError:
                    return
            else:
                try:
                    card = self._get_lowest_hp(self.player_in_play[0])
                except IndexError:
                    return
        low_hp_card = self._get_lowest_hp(card)
        low_hp_card.hp -= dmg_summary[constants.DAMAGE]

    def _handle_lowest_hp_for_heals(self, dmg_summary):
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
        low_hp_card.receive_heal(dmg_summary[constants.HEAL])

    def _handle_conditionals(self, dmg_summary, def_hero):
        if dmg_summary[constants.TARGET] is constants.CARD_ACROSS:
            if dmg_summary[constants.CONDITION] is constants.CONDITION_TYPE:
                if self.def_card.card_type == \
                        dmg_summary[constants.CONDITION_PARAMETER]:
                    dmg_summary[constants.DAMAGE] = dmg_summary[
                        constants.DAMAGE][1]
                else:
                    dmg_summary[constants.DAMAGE] = dmg_summary[
                        constants.DAMAGE][0]
            if self.def_card is None or self.def_card.is_dead():
                self._direct_damage(dmg_summary, def_hero)
                return
            starting_hp = self.def_card.hp
            reflect_summary = self.def_card.handle_abilities_defense(
                dmg_summary)
            self.card.hp -= self._handle_reflect_summary(reflect_summary)
            if dmg_summary.get(constants.EXTRA_EFFECT) is \
                    constants.BLOODTHIRSTY and \
                    starting_hp - self.def_card.hp > 0:
                self.card.handle_bloodthirsty()

    def _handle_heal(self, dmg_summary):
        if dmg_summary[constants.TARGET] is constants.CARD_LOWEST_HP_ALLY:
            self._handle_lowest_hp_for_heals(dmg_summary)

    def _handle_random_damage(self, dmg_summary):
        num_of_targets = dmg_summary.get(constants.NUM_OF_TARGETS, 0)
        if self.player_turn:
            possible_choices = copy(self.opp_in_play)
        else:
            possible_choices = copy(self.player_in_play)
        for target in range(0, num_of_targets):
            if len(possible_choices) == 0:
                return
            card = random.choice(possible_choices)
            possible_choices.remove(card)
            if dmg_summary[constants.EFFECT_TYPE] is constants.DESTROY:
                self._destroy_card(card)
            else:
                reflect_summary = card.handle_abilities_defense(dmg_summary)
                self.card.hp -= self._handle_reflect_summary(reflect_summary)

    def _handle_damage_to_all(self, dmg_summary):
        if dmg_summary[constants.EFFECT_TYPE] in constants.PERSISTENT_EFFECTS:
            if self.player_turn:
                for card in self.opp_in_play:
                    card.add_effect(dmg_summary)
            else:
                for card in self.player_in_play:
                    card.add_effect(dmg_summary)
        else:
            if self.player_turn:
                for card in self.opp_in_play:
                    card.handle_abilities_defense(dmg_summary)
            else:
                for card in self.player_in_play:
                    card.handle_abilities_defense(dmg_summary)

    def _handle_trap(self, dmg_summary):
        if dmg_summary[constants.TARGET] is constants.ENEMY_MULTIPLE:
            num_of_targets = dmg_summary.get(constants.NUM_OF_TARGETS, 0)
            if self.player_turn:
                possible_choices = deepcopy(self.opp_in_play)
            else:
                possible_choices = deepcopy(self.player_in_play)
            for target in range(0, num_of_targets):
                if len(possible_choices) == 0:
                    return
                card = random.choice(possible_choices)
                possible_choices.remove(card)
                card.add_effect(dmg_summary)

    def _handle_laceration(self, dmg_summary):
        if dmg_summary[constants.TARGET] is constants.CARD_ACROSS:
            self.def_card.add_effect(dmg_summary)

    def _handle_bite(self, dmg_summary):
        if self.player_turn:
            card = random.choice(self.opp_in_play)
        else:
            card = random.choice(self.player_in_play)
        starting_hp = card.hp
        card.handle_abilities_defense(dmg_summary)
        self.card.receive_heal(starting_hp - card.hp)

    def _handle_bloodsucker(self, dmg_summary):
        starting_hp = self.def_card.hp
        reflect_summary = self.def_card.handle_abilities_defense(dmg_summary)
        self.card.hp -= self._handle_reflect_summary(reflect_summary)
        heal_amount = (starting_hp - self.def_card.hp) *\
            dmg_summary[constants.PERCENT_DAMAGE_DONE]
        self.card.receive_heal(heal_amount)
        self.def_card.hp += dmg_summary[constants.PERCENT_DAMAGE_DONE]

    def _resolve_damage_to_card_across(self, dmg_summary, def_hero):
        if self.def_card is None or self.def_card.is_dead():
            self._direct_damage(dmg_summary, def_hero)
            return
        if dmg_summary[constants.EFFECT_TYPE] is constants.EXILE:
            self._exile_card(self.def_card)
            self.def_card = None
            return

        starting_hp = self.def_card.hp
        reflect_summary = self.def_card.handle_abilities_defense(dmg_summary)
        self.card.hp -= self._handle_reflect_summary(reflect_summary)
        if dmg_summary.get(constants.EXTRA_EFFECT) is constants.BLOODTHIRSTY \
                and starting_hp - self.def_card.hp > 0:
            self.card.handle_bloodthirsty()

    def _handle_damage_to_card_adjacent(self, dmg_summary):
        cards = self._get_adj_cards(self.card)
        reflect_summary = self.def_card.handle_abilities_defense(dmg_summary)
        self.card.hp -= self._handle_reflect_summary(reflect_summary)
        for card in cards:
            if card == self.card:
                continue
            card.hp -= dmg_summary[constants.DAMAGE]

    def _resolve_damage_through_cards(self, dmg_summary, def_hero):
        if dmg_summary[constants.EFFECT_TYPE] is constants.HEAL:
            self._handle_heal(dmg_summary)
            return
        if dmg_summary[constants.EFFECT_TYPE] is constants.ATK_COND:
            self._handle_conditionals(dmg_summary, def_hero)
            return
        if dmg_summary[constants.EFFECT_TYPE] is constants.LACERATION:
            self._handle_laceration(dmg_summary)
            return
        if dmg_summary[constants.EFFECT_TYPE] is constants.BITE:
            self._handle_bite(dmg_summary)
            return
        if dmg_summary[constants.EFFECT_TYPE] is constants.BLOODSUCKER:
            self._handle_bloodsucker(dmg_summary)
            return
        if dmg_summary[constants.TARGET] is constants.ENEMY_HERO:
            self._direct_damage(dmg_summary, def_hero)
            return
        if dmg_summary[constants.TARGET] is constants.CARD_LOWEST_HP:
            self._handle_lowest_hp_for_dmg(dmg_summary)
            return
        if dmg_summary[constants.TARGET] is constants.ENEMY_RANDOM:
            self._handle_random_damage(dmg_summary)
            return
        if dmg_summary[constants.TARGET] is constants.ALL_ENEMY_CARDS:
            self._handle_damage_to_all(dmg_summary)
            return
        if dmg_summary[constants.TARGET] is constants.CARD_ADJACENT:
            self._handle_damage_to_card_adjacent(dmg_summary)
            return
        if dmg_summary[constants.EFFECT_TYPE] is constants.TRAP:
            self._handle_trap(dmg_summary)
            return
        if self.def_card is None:
            self._direct_damage(dmg_summary, def_hero)
            return
        if dmg_summary[constants.TARGET] is constants.CARD_ACROSS:
            self._resolve_damage_to_card_across(dmg_summary, def_hero)

    def _direct_damage(self, dmg_summary, def_hero):
        dmg_done = 0
        if isinstance(dmg_summary, dict):
            if dmg_summary[constants.EFFECT_TYPE] is constants.ATK_COND:
                dmg_summary[constants.DAMAGE] = dmg_summary[
                    constants.DAMAGE][0]
            if dmg_summary[constants.TARGET] in \
                    (constants.ENEMY_HERO, constants.CARD_ACROSS):
                dmg_done += dmg_summary[constants.DAMAGE]
        elif isinstance(dmg_summary, (list, tuple)):
            for dmg in dmg_summary:
                if dmg[constants.EFFECT_TYPE] not in \
                        constants.CAN_DAMAGE_PLAYER:
                    continue
                if dmg[constants.EFFECT_TYPE] is constants.ATK_COND:
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
            self._resolve_all_healths()

    def _attack_with_card(self, opp, opp_in_play):
        dmg_summary = self.card.handle_abilities_offense()
        if len(opp_in_play) <= self.index:
            self._direct_damage(dmg_summary, opp)
        elif len(opp_in_play) > self.index:
            self.def_card = opp_in_play[self.index]
            self._damage_through_cards(dmg_summary, opp)

    def _handle_all_allies(self, summary):
        if summary[constants.EFFECT_TYPE] is constants.ATK_BUFF:
            if self.player_turn:
                for card in self.player_in_play:
                    card.atk += summary[constants.EFFECT]
        elif summary[constants.EFFECT_TYPE] is constants.ATK_PERCENTBUFF:
            if self.player_turn:
                for card in self.player_in_play:
                    card.atk *= 1 + summary[constants.EFFECT]

    def _handle_rune_effect(self, summary):
        if summary[constants.TARGET] is constants.ALL_ALLY_CARDS:
            self._handle_all_allies(summary)
            return
        if summary[constants.TARGET] is constants.CARD_LOWEST_HP:
            self._handle_lowest_hp_for_dmg(summary)
            return

    def _check_card_in_cemetary(self, condition):
        card_type = condition[constants.CARD_TYPE]
        count = 0
        if self.player_turn:
            for card in self.player_cemetery:
                if card.card_type is card_type:
                    count += 1
            if count >= condition[constants.NUM_TO_ACTIVATE]:
                return True
        else:
            for card in self.opp_cemetery:
                if card.card_type is card_type:
                    count += 1
            if count >= condition[constants.NUM_TO_ACTIVATE]:
                return True
        return False

    def _rune_should_trigger(self, rune):
        if rune.times_triggered > rune.max_times:
            return False
        triggering_conditions = rune.get_triggering_conditions()
        for condition in triggering_conditions:
            if condition[constants.TRIGGERING_CONDITION] is \
                    constants.CARD_IN_CEMETARY:
                return self._check_card_in_cemetary(condition)
            if condition[constants.TRIGGERING_CONDITION] is \
                    constants.EXCEEDED_ROUNDS:
                return self.turn > condition[constants.NUM_TO_ACTIVATE]

    def _handle_runes(self):
        if self.player_turn:
            for rune in self.player.runes:
                if self._rune_should_trigger(rune):
                    rune_effects = rune.get_effect()
                    for effect in rune_effects:
                        self._handle_rune_effect(effect)
                    rune.times_triggered += 1
        else:
            for rune in self.opp.runes:
                if self._rune_should_trigger(rune):
                    rune_effects = rune.get_effect()
                    for effect in rune_effects:
                        self._handle_rune_effect(effect)
                    rune.times_triggered += 1

    def _prep_turn(self):
        self._put_cards_in_play()
        self._put_cards_on_deck()

    def _get_longest_wait_time(self, on_deck):
        if len(on_deck) == 0:
            return
        long_card = on_deck[0]
        for card in on_deck:
            if card.wait > long_card.wait:
                long_card = card
        return long_card

    def _handle_teleportation(self):
        if self.player_turn:
            card = self._get_longest_wait_time(self.opp_on_deck)
        else:
            card = self._get_longest_wait_time(self.player_on_deck)
        if card is None:
            return
        if card.resists_teleportation():
            return
        self._put_card_in_cemetery_from_deck(card)

    def _handle_effect(self, effect):
        if effect.get(constants.TARGET) is constants.OTHER_FOREST_ALLIES:
            if self.player_turn:
                for card in self.player_in_play:
                    if card.card_type == constants.FOREST:
                        card.atk += effect[constants.EFFECT]
        if effect.get(constants.TARGET) is constants.OTHER_TUNDRA_ALLIES:
            if self.player_turn:
                for card in self.player_in_play:
                    if card.card_type == constants.TUNDRA:
                        card.atk += effect[constants.EFFECT]
        if effect.get(constants.EFFECT_TYPE) is constants.TELEPORTATION:
            self._handle_teleportation()

    def _handle_entering_effects(self, card):
        enter_summary = card.enter_effect()
        for effect in enter_summary:
            self._handle_effect(effect)

    def _put_cards_in_play(self):
        self._reduce_wait()
        if self.player_turn:
            for card in self.player_on_deck:
                if card.wait == 0:
                    self.player_in_play.append(card)
                    self._handle_entering_effects(card)
            for card in self.player_in_play:
                if card in self.player_on_deck:
                    self.player_on_deck.remove(card)
        else:
            for card in self.opp_on_deck:
                if card.wait == 0:
                    self.opp_in_play.append(card)
                    self._handle_entering_effects(card)
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
