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

    def get_base_hp(self):
        return self._get_base_hp()

    def _get_base_hp(self):
        return 100000

    def _get_atk(self):
        raise NotImplementedError('This card must have an attack.')


class SeaKing(Demon):
    card_type = constants.DEMON
    stars = 5
    cost = 99
    wait = 4
    starting_wait = 4

    def _get_atk(self):
        return 1200

    def handle_abilities_defense(self, dmg_summary):
        if self.hp <= 0 or dmg_summary[constants.EFFECT_TYPE] in \
                constants.IMMUNITY_EFFECT_TYPES:
            reflect_summary = [
                {
                    constants.EFFECT_TYPE: None,
                    constants.DAMAGE: 0,
                    constants.TARGET: None
                }
            ]
            return reflect_summary
        self.hp -= dmg_summary[constants.DAMAGE]
        reflect_summary = [
            {
                constants.EFFECT_TYPE: constants.ATTACK,
                constants.DAMAGE: abilities.CounterAttack(10).get_effect(),
                constants.TARGET: constants.CARD_ADJACENT
            }
        ]
        return reflect_summary

    def handle_abilities_offense(self):
        exile = abilities.Exile()
        devils_blade = abilities.DevilsBlade()
        dmg_summary = [
            {
                constants.EFFECT_TYPE: exile.effect_type,
                constants.DAMAGE: 0,
                constants.TARGET: exile.target
            },
            {
                constants.EFFECT_TYPE: devils_blade.effect_type,
                constants.DAMAGE: abilities.DevilsBlade().get_effect(),
                constants.TARGET: devils_blade.target
            },
            {
                constants.EFFECT_TYPE: constants.ATTACK,
                constants.DAMAGE: self._get_atk(),
                constants.TARGET: constants.CARD_ACROSS
            }
        ]
        return dmg_summary

    def __str__(self):
        return 'Sea King - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)

    def __repr__(self):
        return 'Sea King - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)


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
            reflect_summary = [
                {
                    constants.EFFECT_TYPE: None,
                    constants.DAMAGE: 0,
                    constants.TARGET: None
                }
            ]
            return reflect_summary
        self.hp -= dmg_summary[constants.DAMAGE]
        retaliation = abilities.Retaliation(10)
        reflect_summary = [
            {
                constants.EFFECT_TYPE: retaliation.effect_type,
                constants.DAMAGE: retaliation.get_effect(),
                constants.TARGET: retaliation.target
            }
        ]
        return reflect_summary

    def handle_abilities_offense(self):
        devils_curse = abilities.DevilsCurse()
        dmg_summary = [
            {
                constants.EFFECT_TYPE: devils_curse.effect_type,
                constants.DAMAGE: devils_curse.get_effect(),
                constants.TARGET: devils_curse.target
            },
            {
                constants.EFFECT_TYPE: constants.ATTACK,
                constants.DAMAGE: self._get_atk(),
                constants.TARGET: constants.CARD_ACROSS
            }
        ]
        return dmg_summary

    def __str__(self):
        return 'Dark Titan - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)

    def __repr__(self):
        return 'Dark Titan - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)
