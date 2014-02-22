import constants
import abilities
from player import Player
from cards import Card


class DemonPlayer(Player):
    def __init__(self):
        super(DemonPlayer, self).__init__(lvl=100)

    def _num_of_cards_allowed(self):
        return 1

    def _num_of_cost_allowed(self):
        return 99

    def __repr__(self):
        return 'Demon Hero - Level: {}  HP: {}'.format(self.lvl, self.hp)


class Demon(Card):
    def __init__(self):
        super(Demon, self).__init__(lvl=10)

    def _get_base_hp(self):
        return 100000

    def _get_atk(self):
        raise NotImplementedError('This card must have an attack.')


class DarkTitan(Demon):
    card_type = constants.DEMON
    stars = 5
    cost = 99
    wait = 4

    def _get_atk(self):
        return 1800

    def handle_abilities_defense(self, dmg_summary):
        if self.hp <= 0 or dmg_summary[constants.EFFECT_TYPE] in \
                constants.IMMUNITY_EFFECT_TYPES:
            return constants.NO_REFLECTED_DAMAGE
        self.hp -= dmg_summary[constants.DAMAGE]
        return abilities.Retaliation(10).get_effect()

    def handle_abilities_offense(self):
        dmg_summary = [
            {
                constants.EFFECT_TYPE: constants.ENEMY_HERO,
                constants.DAMAGE: abilities.DevilsCurse().get_effect()
            },
            {
                constants.EFFECT_TYPE: constants.ATTACK,
                constants.DAMAGE: self._get_atk()
            }
        ]
        return dmg_summary

    def __str__(self):
        return 'Dark Titan - Level: {}  HP: {}  ATK: {}  Wait: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)

    def __repr__(self):
        return 'Dark Titan - Level: {}  HP: {}  ATK: {}  Wait: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)
