from math import floor


class Player():
    def __init__(self, level=None):
        if level <= 0:
            raise ValueError('Player level must be 1 or greater.')
        self.level = level
        self.hp = self._get_health()
        self.cards = list()
        self.shuffled_cards_in_deck = list()
        self.runes = list()

    def _get_health(self):
        # breaking point for health increases
        breaking_point = int(floor((self.level - 1)/10 + 1)*10)
        base_inc = 60
        base_hp = 400
        base_hp_inc = 200

        for i in range(0, floor(breaking_point/10)):
            base_hp += (i + 3) * base_hp_inc

        final_hp = base_hp + (base_inc + breaking_point) * \
          (self.level - (1 + breaking_point - 10))
        return final_hp

    def _total_cost_allowed(self):
        cost = 10
        for i in range(0, self.level):
            if i < 20:
                cost += 3
            elif i < 50:
                cost += 2
            else:
                cost += 1
        return cost

    def get_num_of_cards_allowed(self):
        return self._num_of_cards_allowed_in_deck()

    def get_num_of_runes_allowed(self):
        return self._num_of_runes_allowed()

    def _num_of_cards_allowed_in_deck(self):
        num_of_cards = 3
        if self.level >= 3:
            num_of_cards += 1
        if self.level >= 5:
            num_of_cards += 1
        if self.level >= 10:
            num_of_cards += 1
        if self.level >= 20:
            num_of_cards += 1
        if self.level >= 30:
            num_of_cards += 1
        if self.level >= 35:
            num_of_cards += 1
        if self.level >= 40:
            num_of_cards += 1
        return num_of_cards

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
        if len(self.cards) + 1 > self._num_of_cards_allowed_in_deck():
            raise OverflowError('Too many cards for this level of player.')

        cost = new_card.cost
        for card in self.cards:
            cost += card.cost
        if cost > self._total_cost_allowed():
            print('player: {}'.format(self))
            print('cost: {}'.format(cost))
            print('cards: {}'.format(self.cards))
            print('new card: {}'.format(new_card))
            print('player cost allowed: {}'.format(self._total_cost_allowed()))
            raise OverflowError(
                'Cards cost too much for this level of player.')

        self.cards.append(new_card)

    def __repr__(self):
        return 'Player Hero - Level: {}  HP: {}'.format(self.level, self.hp)

