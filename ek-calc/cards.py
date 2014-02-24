import random

import abilities
import constants


class Card():
    should_res = False
    stunned = False
    prevention = False
    first_attack = True
    base_atk = 0
    hp_inc = 0
    base_hp = 0
    atk_inc = 0

    def __init__(self, lvl=0):
        self.lvl = lvl
        self.hp = self.get_base_hp()
        self.atk = self._get_atk()

    def get_base_hp(self):
        return self.base_hp + self.hp_inc * self.lvl

    def enter_effect(self):
        return list()

    def exit_effect(self):
        return list()

    def _get_atk(self):
        return self.base_atk + self.atk_inc * self.lvl

    def handle_abilities_offense(self):
        raise NotImplementedError('This card must have offensive abilities.')

    def handle_abilities_defense(self, dmg_summary):
        raise NotImplementedError('This card must have defensive abilities.')

    def is_dead(self):
        return self.hp <= 0

    def _handle_effects(self):
        if self.stunned:
            self.stunned = False
            return True
        if self.prevention:
            self.prevention = False
            return False

    def __str__(self):
        raise NotImplementedError(
            'Define how this card will display in results')

    def __repr__(self):
        raise NotImplementedError(
            'Define how this card will display in results')


class HeadlessHorseman(Card):
    def __init__(self, lvl=0):
        self.card_type = constants.MOUNTAIN
        self.stars = 3
        self.wait = 2
        self.starting_wait = 2
        self.cost = 9
        self.base_hp = 590
        self.hp_inc = 8
        self.base_atk = 165
        self.atk_inc = 29
        super(HeadlessHorseman, self).__init__(lvl)

    def handle_abilities_defense(self, dmg_summary):
        self.hp -= abilities.Dodge(3).get_effect() * \
                   dmg_summary[constants.DAMAGE]
        self.stunned = dmg_summary.get(constants.STUN, 0) > \
            random.uniform(0, 1)
        self.prevention = dmg_summary.get(constants.ATTACK_PREVENTION, 0) > \
            random.uniform(0, 1)
        reflect_summary = [
            {
                constants.EFFECT_TYPE: None,
                constants.DAMAGE: 0,
                constants.TARGET: None
            }
        ]
        return reflect_summary

    def handle_abilities_offense(self):
        dmg = self.atk
        if self.lvl >= 5:
            if self.first_attack:
                dmg += abilities.Backstab(3).get_effect()
                self.first_attack = False
        if self.lvl == 10:
            dmg += self.atk * abilities.Concentration(7).get_effect()
        dmg_summary = [{
            constants.EFFECT_TYPE: constants.ATTACK,
            constants.DAMAGE: dmg,
            constants.TARGET: constants.CARD_ACROSS
        }]
        if self.stunned or self.prevention:
            self._handle_effects()
            return list()
        self._handle_effects()
        return dmg_summary

    def __str__(self):
        return 'Headless Horseman - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)

    def __repr__(self):
        return 'Headless Horseman - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)


class SkeletonKing(Card):
    def __init__(self, lvl=0):
        self.card_type = constants.MOUNTAIN
        self.stars = 5
        self.wait = 2
        self.starting_wait = 2
        self.cost = 15
        self.base_hp = 1050
        self.hp_inc = 40
        self.base_atk = 225
        self.atk_inc = 40
        super(SkeletonKing, self).__init__(lvl)

    def handle_abilities_defense(self, dmg_summary):
        self.hp -= dmg_summary[constants.DAMAGE]
        self.stunned = dmg_summary.get(constants.STUN, 0) > \
            random.uniform(0, 1)
        self.prevention = dmg_summary.get(constants.ATTACK_PREVENTION, 0) > \
            random.uniform(0, 1)
        if self.hp <= 0 and self.lvl == 10:
            if abilities.Resurrection(7).get_effect():
                self.should_res = True
        reflect_summary = [
            {
                constants.EFFECT_TYPE: None,
                constants.DAMAGE: 0,
                constants.TARGET: None
            }
        ]
        return reflect_summary

    def handle_abilities_offense(self):
        snipe = abilities.Snipe(9)
        dmg_summary = [{
            constants.EFFECT_TYPE: snipe.effect_type,
            constants.DAMAGE: snipe.get_effect(),
            constants.TARGET: snipe.target
        }]
        dmg = self.atk
        if self.lvl >= 5:
            if self.first_attack:
                dmg += abilities.Backstab(8).get_effect()
                self.first_attack = False
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATTACK,
            constants.DAMAGE: dmg,
            constants.TARGET: constants.CARD_ACROSS
        }
        if self.stunned:
            self._handle_effects()
            return list()
        if self.prevention:
            self._handle_effects()
            return dmg_summary
        dmg_summary.append(for_dmg)
        self._handle_effects()
        return dmg_summary

    def __str__(self):
        return 'Skeleton King - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)

    def __repr__(self):
        return 'Skeleton King - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)


class SpitfireWorm(Card):
    def __init__(self, lvl=0):
        self.card_type = constants.FOREST
        self.stars = 3
        self.wait = 4
        self.starting_wait = 4
        self.cost = 9
        self.base_hp = 600
        self.hp_inc = 17
        self.base_atk = 135
        self.atk_inc = 26
        super(SpitfireWorm, self).__init__(lvl)

    def enter_effect(self):
        forest_force = abilities.ForestForce(4)
        effect_summary = [{
            constants.TARGET: forest_force.target,
            constants.EFFECT: forest_force.get_effect()
        }]
        return effect_summary

    def exit_effect(self):
        forest_force = abilities.ForestForce(4)
        effect_summary = [{
            constants.TARGET: forest_force.target,
            constants.EFFECT: -1 * forest_force.get_effect()
        }]
        return effect_summary

    def handle_abilities_defense(self, dmg_summary):
        self.hp -= dmg_summary[constants.DAMAGE]
        self.stunned = dmg_summary.get(constants.STUN, 0) > \
            random.uniform(0, 1)
        self.prevention = dmg_summary.get(constants.ATTACK_PREVENTION, 0) > \
            random.uniform(0, 1)
        if self.hp <= 0 and self.lvl == 10:
            if abilities.Resurrection(7).get_effect():
                self.should_res = True
        reflect_summary = [
            {
                constants.EFFECT_TYPE: None,
                constants.DAMAGE: 0,
                constants.TARGET: None
            }
        ]
        return reflect_summary

    def handle_abilities_offense(self):
        fireball = abilities.Fireball(3)
        dmg_summary = [{
            constants.EFFECT_TYPE: fireball.effect_type,
            constants.DAMAGE: fireball.get_effect(),
            constants.TARGET: fireball.target,
            constants.NUM_OF_TARGETS: fireball.num_of_targets,
            constants.ELEMENT_TYPE: fireball.element_type
        }]
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATTACK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS
        }
        if self.stunned:
            self._handle_effects()
            return list()
        if self.prevention:
            self._handle_effects()
            if self.lvl >= 5:
                self.hp += abilities.Rejuvenation(4).get_effect()
            return dmg_summary
        self.hp += abilities.Rejuvenation(4).get_effect()
        dmg_summary.append(for_dmg)
        self._handle_effects()
        return dmg_summary

    def __str__(self):
        return 'Spitfire Worm - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)

    def __repr__(self):
        return 'Spitfire Worm - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)


class Troglodyte(Card):
    def __init__(self, lvl=0):
        self.card_type = constants.FOREST
        self.stars = 3
        self.wait = 4
        self.starting_wait = 4
        self.cost = 9
        self.base_hp = 680
        self.hp_inc = 28
        self.base_atk = 180
        self.atk_inc = 23
        super(Troglodyte, self).__init__(lvl)

    def handle_abilities_defense(self, dmg_summary):
        self.hp -= dmg_summary[constants.DAMAGE]
        self.stunned = dmg_summary.get(constants.STUN, 0) > \
            random.uniform(0, 1)
        self.prevention = dmg_summary.get(constants.ATTACK_PREVENTION, 0) > \
            random.uniform(0, 1)
        reflect_summary = [
            {
                constants.EFFECT_TYPE: None,
                constants.DAMAGE: 0,
                constants.TARGET: None
            }
        ]
        return reflect_summary

    def handle_abilities_offense(self):
        healing = abilities.Healing(6)
        dmg_summary = [{
            constants.EFFECT_TYPE: healing.effect_type,
            constants.DAMAGE: healing.get_effect(),
            constants.TARGET: healing.target
        }]
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATTACK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS,
        }
        if self.lvl >= 5:
            swamp_purity = abilities.SwampPurity(5)
            dmg2 = self.atk * (1 + swamp_purity.get_effect())
            for_dmg = {
                constants.EFFECT_TYPE: swamp_purity.effect_type,
                constants.DAMAGE: (self.atk, dmg2),
                constants.TARGET: swamp_purity.target,
                constants.CONDITION: constants.CONDITION_TYPE,
                constants.CONDITION_PARAMETER: constants.SWAMP
            }
        if self.lvl == 10:
            chain_lightning = abilities.ChainLightning(6)
            dmg_summary.append({
                constants.EFFECT_TYPE: chain_lightning.effect_type,
                constants.DAMAGE: chain_lightning.get_effect(),
                constants.TARGET: chain_lightning.target,
                constants.NUM_OF_TARGETS: chain_lightning.num_of_targets,
                constants.ATTACK_PREVENTION: chain_lightning.attack_prevention,
                constants.ELEMENT_TYPE: chain_lightning.element_type
            })
        if self.stunned:
            self._handle_effects()
            return list()
        if self.prevention:
            self._handle_effects()
            return dmg_summary
        dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Troglodyte - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)

    def __repr__(self):
        return 'Troglodyte - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)


class WoodElfArcher(Card):
    def __init__(self, lvl=0):
        self.card_type = constants.FOREST
        self.stars = 2
        self.wait = 2
        self.starting_wait = 2
        self.cost = 5
        self.base_hp = 385
        self.hp_inc = 20
        self.base_atk = 105
        self.atk_inc = 24
        super(WoodElfArcher, self).__init__(lvl)

    def handle_abilities_defense(self, dmg_summary):
        self.hp -= dmg_summary[constants.DAMAGE]
        reflect_summary = [
            {
                constants.EFFECT_TYPE: None,
                constants.DAMAGE: 0,
                constants.TARGET: None
            }
        ]
        return reflect_summary

    def handle_abilities_offense(self):
        snipe = abilities.Snipe(2)
        dmg_summary = [{
            constants.EFFECT_TYPE: snipe.effect_type,
            constants.DAMAGE: snipe.get_effect(),
            constants.TARGET: snipe.target
        }]
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATTACK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS,
        }
        if self.lvl >= 5:
            swamp_purity = abilities.SwampPurity(5)
            dmg2 = self.atk * (1 + swamp_purity.get_effect())
            for_dmg = {
                constants.EFFECT_TYPE: swamp_purity.effect_type,
                constants.DAMAGE: (self.atk, dmg2),
                constants.TARGET: swamp_purity.target,
                constants.CONDITION: constants.CONDITION_TYPE,
                constants.CONDITION_PARAMETER: constants.SWAMP
            }
        if self.lvl == 10:
            snipe = abilities.Snipe(5)
            dmg_summary.append({
                constants.EFFECT_TYPE: snipe.effect_type,
                constants.DAMAGE: snipe.get_effect(),
                constants.TARGET: snipe.target
            })
        if self.stunned:
            self._handle_effects()
            return list()
        if self.prevention:
            self._handle_effects()
            return dmg_summary
        dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Wood Elf Archer - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)

    def __repr__(self):
        return 'Wood Elf Archer - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)
