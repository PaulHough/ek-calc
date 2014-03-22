from math import floor


class Player():
    def __init__(self, level=None):
        if level <= 0:
            raise ValueError('Player level must be 1 or greater.')
        self.level = level
        self.hp = self._get_health()
        self.cards = list()
        self.shuffled_cards_in_deck = list()
        self.number_of_cards_allowed_in_deck = 3
        self.runes = list()
        self.cost = 0

    def _get_health(self):
        breaking_point = int(floor((self.level - 1)/10 + 1)*10) # breaking point for health increases
        base_inc = 60
        base_hp = 400
        base_hp_inc = 200

        for i in range(0, floor(breaking_point/10)):
            base_hp += (i + 3) * base_hp_inc

        final_hp = base_hp + (base_inc + breaking_point) * (self.level - (1 + breaking_point - 10))
        return final_hp

    def _total_cost_allowed(self):

        return 10000 # Skip the rest of this until ready to use. May not be very necessary until sim is more fully developed.

        if self.cost < 10: # Calculate cost for a player only once. Simplified after profiling.

            self.cost = 10

            for i in range(0, self.lvl):
                if i < 20:
                    self.cost += 3
                elif i < 50:
                    self.cost += 2
                else:
                    self.cost += 1
        return self.cost

    def get_num_of_cards_allowed(self):
        return self._num_of_cards_allowed_in_deck()

    def get_num_of_runes_allowed(self):
        return self._num_of_runes_allowed()

    def _num_of_cards_allowed_in_deck(self):
        if self.number_of_cards_allowed_in_deck == 3:
            if self.level >= 3:
                self.number_of_cards_allowed_in_deck += 1
            if self.level >= 5:
                self.number_of_cards_allowed_in_deck += 1
            if self.level >= 10:
                self.number_of_cards_allowed_in_deck += 1
            if self.level >= 20:
                self.number_of_cards_allowed_in_deck += 1
            if self.level >= 30:
                self.number_of_cards_allowed_in_deck += 1
            if self.level >= 35:
                self.number_of_cards_allowed_in_deck += 1
            if self.level >= 40:
                self.number_of_cards_allowed_in_deck += 1
        return self.number_of_cards_allowed_in_deck

    def _num_of_runes_allowed(self):
        if self.level < 50:
            return int(floor(self.level/10))
        return 4

    def assign_rune(self, new_rune):
        if len(self.runes) + 1 > self._num_of_runes_allowed():
            raise OverflowError('Too many runes for this level of player.')
        for rune in self.runes:
            if new_rune.name == rune.name:
                raise ValueError('Only one of each rune is allowed.')
        self.runes.append(new_rune)

    def assign_card(self, new_card):
        number_of_cards_i_will_have_after_card_addition = len(self.cards) + 1
        if number_of_cards_i_will_have_after_card_addition > self._num_of_cards_allowed_in_deck():
            raise OverflowError('Too many cards in the deck for this level of player.')

        cost = 0
        for card in self.cards:
            cost += card.cost
        if cost > self._total_cost_allowed():
            raise OverflowError(
                'Cards cost too much for this level of player.')

        self.cards.append(new_card)

    def __repr__(self):
        return 'Player Hero - Level: {}  HP: {}'.format(self.level, self.hp)

