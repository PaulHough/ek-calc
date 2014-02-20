from sys import maxsize

import constants
import abilities
from player import Player


class DemonPlayer(Player):
    def _num_of_cards_allowed(self):
        return 1

    def _num_of_cost_allowed(self):
        return 99


class Demon():
    def __init__(self):
        self.rank = 10
        self.hp = self._get_hp()
        self.atk = self._get_atk()

    @staticmethod
    def _get_hp():
        return maxsize

    def _get_atk(self):
        raise NotImplementedError('This card must have an attack.')


class DarkTitan(Demon):
    card_type = constants.DEMON
    stars = 5
    cost = 99
    wait = 4
    abilities = (abilities.Retaliation(10), abilities.DevilsCurse(),
                 abilities.Laceration(), abilities.Immunity())

    def _get_atk(self):
        return 1800

