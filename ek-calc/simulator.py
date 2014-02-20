import random


class Fight():
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.turn = 0
        self.results = dict()
        self.sim_fight()

    def sim_fight(self):
        self._prep_cards()
        while self.player.hp > 0 and self.enemy.hp > 0:
            pass

    def _prep_cards(self):
        cards_to_order = self.player.cards
        while len(self.player.card_order) != len(cards_to_order):
            card_index = random.choice(range(0, cards_to_order))
