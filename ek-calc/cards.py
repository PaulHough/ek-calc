import abilities
import constants


class Card():
    def __init__(self, lvl):
        self.lvl = lvl
        self.hp = self._get_hp()
        self.atk = self._get_atk()

    def _get_hp(self):
        raise NotImplementedError('This card must have health.')

    def _get_atk(self):
        raise NotImplementedError('This card must have an attack.')


class HeadlessHorseman(Card):
    card_type = constants.MOUNTAIN
    stars = 3
    wait = 2
    cost = 9
    abilities = (abilities.Dodge(3), abilities.Backstab(3),
                 abilities.Concentration(7))

    def _get_hp(self):
        base_hp = 590
        hp_inc = 8
        return base_hp + hp_inc * self.lvl

    def _get_atk(self):
        base_atk = 165
        atk_inc = 29
        return base_atk + atk_inc * self.lvl

