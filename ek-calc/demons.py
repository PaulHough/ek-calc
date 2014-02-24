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
        self.card_type = constants.DEMON
        self.starts = 5
        self.cost = 99
        self.wait = 4
        self.starting_wait = 4
        self.base_hp = 0
        self.hp_inc = 0
        self.base_atk = 0
        self.atk_inc = 0
        super(Demon, self).__init__(lvl=10)

    def get_base_hp(self):
        return 100000


class DarkTitan(Demon):
    def _get_atk(self):
        return 1800

    def handle_abilities_defense(self, dmg_summary):
        if self.hp <= 0 or dmg_summary.get(constants.ELEMENT_TYPE, '') in \
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
                constants.DAMAGE: self.atk,
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


class Deucalion(Demon):
    def _get_atk(self, base=None, inc=None):
        return 900

    def handle_abilities_defense(self, dmg_summary):
        if self.hp <= 0 or dmg_summary.get(constants.ELEMENT_TYPE, '') in \
                constants.IMMUNITY_EFFECT_TYPES:
            return list()
        parry = abilities.Parry(10)
        dmg_done = dmg_summary[constants.DAMAGE] - parry.get_effect()
        if dmg_done > 0:
            self.hp -= dmg_done
            devils_armor = abilities.DevilsArmor()
            return [
                {
                    constants.EFFECT_TYPE: devils_armor.effect_type,
                    constants.DAMAGE: devils_armor.get_effect(),
                    constants.TARGET: devils_armor.target,
                }
            ]
        return list()

    def handle_abilities_offense(self):
        exile = abilities.Exile()
        dmg_summary = [
            {
                constants.EFFECT_TYPE: exile.effect_type,
                constants.DAMAGE: 0,
                constants.TARGET: exile.target
            },
            {
                constants.EFFECT_TYPE: constants.ATTACK,
                constants.DAMAGE: self.atk,
                constants.TARGET: constants.CARD_ACROSS
            }
        ]
        return dmg_summary

    def __str__(self):
        return 'Deucalion - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)

    def __repr__(self):
        return 'Deucalion - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)


class SeaKing(Demon):
    def _get_atk(self, base=None, inc=None):
        return 1200

    def handle_abilities_defense(self, dmg_summary):
        if self.hp <= 0 or dmg_summary.get(constants.ELEMENT_TYPE, '') in \
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
        counter_attack = abilities.CounterAttack(10)
        reflect_summary = [
            {
                constants.EFFECT_TYPE: counter_attack.effect_type,
                constants.DAMAGE: counter_attack.get_effect(),
                constants.TARGET: counter_attack.target
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
                constants.DAMAGE: devils_blade.get_effect(),
                constants.TARGET: devils_blade.target
            },
            {
                constants.EFFECT_TYPE: constants.ATTACK,
                constants.DAMAGE: self.atk,
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
