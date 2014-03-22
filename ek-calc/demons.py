import constants
import abilities
from player import Player
from cards import Card


class DemonPlayer(Player):
    def __init__(self, level=1000):
        super(DemonPlayer, self).__init__(level)

    def _num_of_cards_allowed(self):
        return 1

    def _num_of_cost_allowed(self):
        return 99

    def __repr__(self):
        return 'Demon Hero - Level: {}  HP: {}'.format(self.level, self.hp)


class Demon(Card):
    def __init__(self, level=10, merit=False):
        self.card_type = constants.DEMON
        self.starts = 5
        self.cost = 99
        self.wait = 4
        self.starting_wait = 4
        self.base_hp = 0
        self.hp_inc = 0
        self.base_atk = 0
        self.atk_inc = 0
        self.immune = True
        super(Demon, self).__init__(level, merit)

    def _get_base_hp(self):
        return 10000000 ## TODO: The sim doesn't handle it well when the Demon dies.

    def _handle_lvl_5_ability(self):
        pass

    def _handle_lvl_10_ability(self):
        pass

    def add_effect(self, dmg_summary):
        pass


class DarkTitan(Demon):
    def _get_base_atk(self, base=None, inc=None):
        return 1800

    def _get_reflect_summary(self, dmg_summary):
        if self.hp <= 0 or dmg_summary[constants.EFFECT_TYPE] in \
                constants.IMMUNITY_EFFECT_TYPES:
            return list()
        self.hp -= dmg_summary[constants.DAMAGE]
        retaliation = abilities.Retaliation(10)
        return [{
            constants.EFFECT_TYPE: retaliation.effect_type,
            constants.DAMAGE: retaliation.get_effect(),
            constants.TARGET: retaliation.target
        }]

    def _get_damage_summary(self):
        devils_curse = abilities.DevilsCurse()
        laceration = abilities.Laceration()
        return [{
            constants.EFFECT_TYPE: devils_curse.effect_type,
            constants.DAMAGE: devils_curse.get_effect(),
            constants.TARGET: devils_curse.target
        }, {
            constants.EFFECT_TYPE: laceration.effect_type,
            constants.TARGET: laceration.target,
            constants.REMAINING: None
        }, {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS
        }]

    def __str__(self):
        return 'Dark Titan - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)

    def __repr__(self):
        return 'Dark Titan - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)


class Deucalion(Demon):
    def _get_base_atk(self, base=None, inc=None):
        return 900

    def _get_reflect_summary(self, dmg_summary):
        if self.hp <= 0 or dmg_summary[constants.EFFECT_TYPE] in \
                constants.IMMUNITY_EFFECT_TYPES:
            return list()
        parry = abilities.Parry(10)
        dmg_done = dmg_summary[constants.DAMAGE] - parry.get_effect()
        if dmg_done > 0:
            self.hp -= dmg_done
            devils_armor = abilities.DevilsArmor()
            return [{
                constants.EFFECT_TYPE: devils_armor.effect_type,
                constants.DAMAGE: devils_armor.get_effect(),
                constants.TARGET: devils_armor.target,
            }]
        return list()

    def _get_damage_summary(self):
        exile = abilities.Exile()
        return [{
            constants.EFFECT_TYPE: exile.effect_type,
            constants.DAMAGE: 0,
            constants.TARGET: exile.target
        }, {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS
        }]

    def __str__(self):
        return 'Deucalion - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)

    def __repr__(self):
        return 'Deucalion - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)


class Mars(Demon):
    def _get_base_atk(self, base=None, inc=None):
        return 1200

    def _get_reflect_summary(self, dmg_summary):
        if self.hp <= 0 or dmg_summary[constants.EFFECT_TYPE] in \
                constants.IMMUNITY_EFFECT_TYPES:
            return list()
        self.hp -= dmg_summary[constants.DAMAGE]
        return list()

    def handle_abilities_offense(self):
        destroy = abilities.Destroy()
        devils_curse = abilities.DevilsCurse()
        fire_god = abilities.FireGod(10)
        return [{
            constants.EFFECT_TYPE: destroy.effect_type,
            constants.DAMAGE: 0,
            constants.TARGET: destroy.target,
            constants.NUM_OF_TARGETS: destroy.num_of_targets
        }, {
            constants.EFFECT_TYPE: devils_curse.effect_type,
            constants.DAMAGE: devils_curse.get_effect(),
            constants.TARGET: devils_curse.target
        }, {
            constants.EFFECT_TYPE: fire_god.effect_type,
            constants.DAMAGE: fire_god.get_effect(),
            constants.TARGET: fire_god.target,
            constants.REMAINING: None
        }, {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS
        }]

    def __str__(self):
        return 'Mars - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)

    def __repr__(self):
        return 'Mars - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)


class Pandarus(Demon):
    def _get_base_atk(self, base=None, inc=None):
        return 1500

    def _get_reflect_summary(self, dmg_summary):
        if self.hp <= 0 or dmg_summary[constants.EFFECT_TYPE] in \
                constants.IMMUNITY_EFFECT_TYPES:
            return list()
        self.hp -= dmg_summary[constants.DAMAGE]
        devils_armor = abilities.DevilsArmor()
        return [{
            constants.EFFECT_TYPE: devils_armor.effect_type,
            constants.DAMAGE: devils_armor.get_effect(),
            constants.TARGET: devils_armor.target,
        }]

    def _get_damage_summary(self):
        curse = abilities.Curse(10)
        toxic_clouds = abilities.ToxicClouds(10)
        return [{
            constants.EFFECT_TYPE: curse.effect_type,
            constants.DAMAGE: curse.get_effect(),
            constants.TARGET: curse.target
        }, {
            constants.EFFECT_TYPE: toxic_clouds.effect_type,
            constants.DAMAGE: toxic_clouds.get_effect(),
            constants.TARGET: toxic_clouds.target
        }, {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS
        }, {
            constants.EFFECT_TYPE: toxic_clouds.effect_type,
            constants.DAMAGE: toxic_clouds.get_effect(),
            constants.TARGET: toxic_clouds.target
        }]

    def __str__(self):
        return 'Pandarus - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)

    def __repr__(self):
        return 'Pandarus - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)


class PlagueOgryn(Demon):
    def _get_base_atk(self, base=None, inc=None):
        return 1500

    def _get_reflect_summary(self, dmg_summary):
        if self.hp <= 0 or dmg_summary[constants.EFFECT_TYPE] in \
                constants.IMMUNITY_EFFECT_TYPES:
            return list()
        self.hp -= dmg_summary[constants.DAMAGE]
        return list()

    def _get_damage_summary(self):
        devils_blade = abilities.DevilsBlade()
        toxic_clouds = abilities.ToxicClouds(10)
        trap = abilities.Trap(5)
        return [{
            constants.EFFECT_TYPE: trap.effect_type,
            constants.TARGET: trap.target,
            constants.NUM_OF_TARGETS: trap.get_effect()
        }, {
            constants.EFFECT_TYPE: devils_blade.effect_type,
            constants.DAMAGE: devils_blade.get_effect(),
            constants.TARGET: devils_blade.target
        }, {
            constants.EFFECT_TYPE: toxic_clouds.effect_type,
            constants.DAMAGE: toxic_clouds.get_effect(),
            constants.TARGET: toxic_clouds.target
        }, {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS
        }, {
            constants.EFFECT_TYPE: toxic_clouds.effect_type,
            constants.DAMAGE: toxic_clouds.get_effect(),
            constants.TARGET: toxic_clouds.target
        }]

    def __str__(self):
        return 'Plague Ogryn - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)

    def __repr__(self):
        return 'Plague Ogryn - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)


class SeaKing(Demon):
    def _get_base_atk(self, base=None, inc=None):
        return 1200

    def _get_reflect_summary(self, dmg_summary):
        if self.hp <= 0 or dmg_summary[constants.EFFECT_TYPE] in \
                constants.IMMUNITY_EFFECT_TYPES:
            return list()
        self.hp -= dmg_summary[constants.DAMAGE]
        counter_attack = abilities.CounterAttack(10)
        return [{
            constants.EFFECT_TYPE: counter_attack.effect_type,
            constants.DAMAGE: counter_attack.get_effect(),
            constants.TARGET: counter_attack.target
        }]

    def _get_damage_summary(self):
        exile = abilities.Exile()
        devils_blade = abilities.DevilsBlade()
        return [{
            constants.EFFECT_TYPE: exile.effect_type,
            constants.DAMAGE: 0,
            constants.TARGET: exile.target
        }, {
            constants.EFFECT_TYPE: devils_blade.effect_type,
            constants.DAMAGE: devils_blade.get_effect(),
            constants.TARGET: devils_blade.target
        }, {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS
        }]

    def __str__(self):
        return 'Sea King - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)

    def __repr__(self):
        return 'Sea King - Level: {}  HP: {}  ATK: {}'.format(
            self.lvl, self.hp, self.atk, self.wait)
