import abilities
import constants


class Card():
    def __init__(self, lvl=0):
        self.lvl = lvl
        self.hp = self._get_hp()
        self.atk = self._get_atk()

    def _get_hp(self):
        raise NotImplementedError('This card must have health.')

    def _get_atk(self):
        raise NotImplementedError('This card must have an attack.')

    def handle_abilities_offense(self):
        raise NotImplementedError('This card must have offensive abilities.')

    def handle_abilities_defense(self, dmg_summary):
        raise NotImplementedError('This card must have defensive abilities.')

    def is_dead(self):
        return self.hp <= 0

    def __str__(self):
        raise NotImplementedError(
            'Define how this card will display in results')

    def __repr__(self):
        raise NotImplementedError(
            'Define how this card will display in results')


class HeadlessHorseman(Card):
    card_type = constants.MOUNTAIN
    stars = 3
    wait = 2
    cost = 9
    first_attack = True

    def _get_hp(self):
        base_hp = 590
        hp_inc = 8
        return base_hp + hp_inc * self.lvl

    def _get_atk(self):
        base_atk = 165
        atk_inc = 29
        return base_atk + atk_inc * self.lvl

    def handle_abilities_defense(self, dmg_summary):
        self.hp -= abilities.Dodge(3).get_effect() * \
                   dmg_summary[constants.DAMAGE]
        return constants.NO_REFLECTED_DAMAGE

    def handle_abilities_offense(self):
        dmg = self._get_atk()
        if self.lvl >= 5:
            if self.first_attack:
                dmg += abilities.Backstab(3).get_effect()
                self.first_attack = False
        if self.lvl == 10:
            dmg += abilities.Concentration(7).get_effect()
        dmg_summary = {
            constants.EFFECT_TYPE: constants.ATTACK,
            constants.DAMAGE: dmg
        }

        return dmg_summary

    def __str__(self):
        return 'Headless Horseman - Level: {}  HP: {}  ATK: {}  Wait: {}'.\
            format(self.lvl, self.hp, self.atk, self.wait)

    def __repr__(self):
        return 'Headless Horseman - Level: {}  HP: {}  ATK: {}  Wait: {}'.\
            format(self.lvl, self.hp, self.atk, self.wait)
