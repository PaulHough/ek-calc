from math import floor


class Player():
    def __init__(self, lvl=None):
        if lvl <= 0:
            raise ValueError('Player level must be 1 or greater.')
        self.lvl = lvl
        self.hp = self._get_health()
        self.cards = list()
        self.card_order = list()
        self.runes = list()

    def _get_health(self):
        bp = int(floor((self.lvl - 1)/10 + 1)*10)
        base_inc = 60
        base_hp = 400
        base_hp_inc = 200
        for i in range(0, floor(bp/10)):
            base_hp += (i + 3) * base_hp_inc
        return base_hp + (base_inc + bp) * (self.lvl - (1 + bp - 10))

    def _num_of_cost_allowed(self):
        cost = 10
        for i in range(0, self.lvl):
            if i < 20:
                cost += 3
            elif i < 50:
                cost += 2
            else:
                cost += 1
        return 10000
        # return cost

    def get_num_of_cards_allowed(self):
        return self._num_of_cards_allowed()

    def get_num_of_runes_allowed(self):
        return self._num_of_runes_allowed()

    def _num_of_cards_allowed(self):
        num_of_cards = 3
        if self.lvl >= 3:
            num_of_cards += 1
        if self.lvl >= 5:
            num_of_cards += 1
        if self.lvl >= 10:
            num_of_cards += 1
        if self.lvl >= 20:
            num_of_cards += 1
        if self.lvl >= 30:
            num_of_cards += 1
        if self.lvl >= 35:
            num_of_cards += 1
        if self.lvl >= 40:
            num_of_cards += 1
        return num_of_cards

    def _num_of_runes_allowed(self):
        if self.lvl < 50:
            return int(floor(self.lvl/10))
        return 4

    def assign_rune(self, new_rune):
        if len(self.runes) + 1 > self._num_of_runes_allowed():
            raise OverflowError('Too many runes for this level of player.')
        for rune in self.runes:
            if new_rune.name == rune.name:
                raise ValueError('Only one of each rune is allowed.')
        self.runes.append(new_rune)

    def assign_card(self, new_card):
        if len(self.cards) + 1 > self._num_of_cards_allowed():
            raise OverflowError('Too many cards for this level of player.')
        cost = 0
        for card in self.cards:
            cost += card.cost
        if cost > self._num_of_cost_allowed():
            raise OverflowError(
                'Cards cost too much for this level of player.')
        self.cards.append(new_card)

    def __repr__(self):
        return 'Player Hero - Level: {}  HP: {}'.format(self.lvl, self.hp)
