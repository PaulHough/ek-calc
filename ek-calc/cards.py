import random

import abilities
import constants


class Card():
    def __init__(self, lvl=0):
        if lvl > 10 or lvl < 0:
            raise ValueError('Cards must have a level 0 to 10.')
        self.lvl = lvl
        self.hp = self.get_base_hp()
        self.atk = self._get_atk()
        self.should_res = False
        self.stunned = False
        self.prevention = False
        self.lacerate = False
        self.first_attack = True
        self.base_atk = 0
        self.hp_inc = 0
        self.base_hp = 0
        self.atk_inc = 0
        self.effects = list()


    def get_base_hp(self):
        return self.base_hp + self.hp_inc * self.lvl

    def enter_effect(self):
        return list()

    def exit_effect(self):
        return list()

    def _get_atk(self):
        return self.base_atk + self.atk_inc * self.lvl

    def add_effect(self, dmg_summary):
        if dmg_summary[constants.EFFECT_TYPE] in constants.STUN_TYPES:
            self.stunned = True
        self.effects.append(dmg_summary)

    def _resolve_effects(self):
        for effect in self.effects:
            if effect.get(constants.REMAINING) is None:
                self.handle_abilities_defense(effect)
            elif effect.get(constants.REMAINING) > 0:
                self.handle_abilities_defense(effect)
                effect[constants.REMAINING] -= 1

    def handle_abilities_offense(self):
        dmg_summary = self._get_damage_summary()
        if self.stunned:
            dmg_summary = list()
        self._resolve_effects()
        self.clear_stun_effects()
        return dmg_summary

    def _handle_lvl_5_ability(self):
        raise NotImplementedError('This card must have a level 5 ability.')

    def _handle_lvl_10_ability(self):
        raise NotImplementedError('This card must have a level 10 ability.')

    def _get_damage_summary(self):
        raise NotImplementedError('This card must have offensive abilities.')

    def handle_bloodthirsty(self):
        pass

    def handle_abilities_defense(self, dmg_summary):
        self._handle_stunning_effects(dmg_summary)
        return self._get_reflect_summary(dmg_summary)

    def _get_reflect_summary(self, dmg_summary):
        self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        return list()

    def is_dead(self):
        return self.hp <= 0

    def clear_stun_effects(self):
        if self.stunned:
            self.stunned = False
            return True
        if self.prevention:
            self.prevention = False
            return False

    def receive_heal(self, heal):
        if self.lacerate:
            return
        self.hp += heal

    def _handle_stunning_effects(self, dmg_summary):
        self.stunned = dmg_summary.get(constants.STUN, 0) > \
            random.uniform(0, 1)
        self.prevention = dmg_summary.get(constants.ATK_PREVENTION, 0) > \
            random.uniform(0, 1)

    def __str__(self):
        raise NotImplementedError(
            'Define how this card will display in results')

    def __repr__(self):
        raise NotImplementedError(
            'Define how this card will display in results')


class BloodWarrior(Card):
    def __init__(self, lvl=0):
        self.card_type = constants.SWAMP
        self.stars = 4
        self.wait = 4
        self.starting_wait = 4
        self.cost = 13
        self.base_hp = 890
        self.hp_inc = 45
        self.base_atk = 250
        self.atk_inc = 24
        super(BloodWarrior, self).__init__(lvl)

    def _get_reflect_summary(self, dmg_summary):
        if self.lvl >= 5 and \
                dmg_summary[constants.EFFECT_TYPE] is constants.SPELL:
            reflection = abilities.Reflection(4)
            return [{
                constants.EFFECT_TYPE: reflection.effect_type,
                constants.DAMAGE: reflection.get_effect(),
                constants.TARGET: reflection.target
            }]
        else:
            self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        return list()

    def _handle_lvl_5_ability(self):
        pass

    def _handle_lvl_10_ability(self):
        pass

    def handle_bloodthirsty(self):
        if self.lvl == 10:
            bloodthirsty = abilities.Bloodthirsty(6)
            self.atk += bloodthirsty.get_effect()

    def _get_damage_summary(self):
        if self.prevention:
            return list()
        arctic_pollution = abilities.ArcticPollution(6)
        dmg2 = self.atk * (1 + arctic_pollution.get_effect())
        return [{
            constants.EFFECT_TYPE: arctic_pollution.effect_type,
            constants.DAMAGE: (self.atk, dmg2),
            constants.TARGET: arctic_pollution.target,
            constants.CONDITION: constants.CONDITION_TYPE,
            constants.CONDITION_PARAMETER: constants.TUNDRA,
            constants.EXTRA_EFFECT: constants.BLOODTHIRSTY
        }]

    def __str__(self):
        return 'Headless Horseman - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)

    def __repr__(self):
        return 'Headless Horseman - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)


class BronzeDragon(Card):
    def __init__(self, lvl=0):
        self.card_type = constants.FOREST
        self.stars = 4
        self.wait = 4
        self.starting_wait = 4
        self.cost = 13
        self.base_hp = 780
        self.hp_inc = 48
        self.base_atk = 200
        self.atk_inc = 20
        super(BronzeDragon, self).__init__(lvl)

    def _get_reflect_summary(self, dmg_summary):
        if self.lvl == 10 and \
                dmg_summary[constants.EFFECT_TYPE] is constants.ATK:
            dodge_chance = abilities.Dodge(8).get_effect()
            self.hp -= dodge_chance * dmg_summary.get(constants.DAMAGE, 0)
        else:
            self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        return list()

    def _handle_lvl_5_ability(self):
        if abilities.Resurrection(6).get_effect():
            self.should_res = True

    def _handle_lvl_10_ability(self):
        pass

    def _get_damage_summary(self):
        thunderbolt = abilities.Thunderbolt(4)
        dmg_summary = [{
            constants.EFFECT_TYPE: thunderbolt.effect_type,
            constants.DAMAGE: thunderbolt.get_effect(),
            constants.TARGET: thunderbolt.target
        }]
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS
        }
        if not self.prevention:
            dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Headless Horseman - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)

    def __repr__(self):
        return 'Headless Horseman - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)


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

    def _get_reflect_summary(self, dmg_summary):
        if dmg_summary[constants.EFFECT_TYPE] is constants.ATK:
            dodge = abilities.Dodge(3).get_effect()
            if dodge:
                return list()
        self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        return list()

    def _handle_lvl_5_ability(self):
        pass

    def _handle_lvl_10_ability(self):
        pass

    def _get_damage_summary(self):
        dmg = self.atk
        if self.lvl >= 5:
            if self.first_attack:
                dmg += abilities.Backstab(3).get_effect()
                self.first_attack = False
        if self.lvl == 10:
            dmg += self.atk * abilities.Concentration(7).get_effect()
        dmg_summary = [{
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: dmg,
            constants.TARGET: constants.CARD_ACROSS
        }]
        if self.prevention:
            return list()
        return dmg_summary

    def __str__(self):
        return 'Headless Horseman - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)

    def __repr__(self):
        return 'Headless Horseman - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)


class Necromancer(Card):
    def __init__(self, lvl=0):
        self.card_type = constants.MOUNTAIN
        self.stars = 4
        self.wait = 4
        self.starting_wait = 4
        self.cost = 13
        self.base_hp = 720
        self.hp_inc = 25
        self.base_atk = 220
        self.atk_inc = 24
        super(Necromancer, self).__init__(lvl)

    def _get_reflect_summary(self, dmg_summary):
        if self.lvl >= 5 and \
                dmg_summary[constants.EFFECT_TYPE] is constants.ATK:
            dodge_chance = abilities.Dodge(6).get_effect()
            self.hp -= dodge_chance * dmg_summary.get(constants.DAMAGE, 0)
        else:
            self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        return list()

    def _handle_lvl_5_ability(self):
        pass

    def _handle_lvl_10_ability(self):
        if abilities.Resurrection(6).get_effect():
            self.should_res = True

    def _get_damage_summary(self):
        bite = abilities.Bite(6)
        dmg_summary = [{
            constants.EFFECT_TYPE: bite.effect_type,
            constants.DAMAGE: bite.get_effect(),
            constants.TARGET: bite.target
        }]
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS
        }
        if not self.prevention:
            dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Necromancer - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)

    def __repr__(self):
        return 'Necromancer - Level: {}  HP: {}  ATK: {}'.\
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

    def _get_reflect_summary(self, dmg_summary):
        self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        if self.hp <= 0 and self.lvl == 10:
            self._handle_lvl_10_ability()
        return list()

    def _handle_lvl_5_ability(self):
        snipe = abilities.Snipe(9)
        return {
            constants.EFFECT_TYPE: snipe.effect_type,
            constants.DAMAGE: snipe.get_effect(),
            constants.TARGET: snipe.target
        }

    def _handle_lvl_10_ability(self):
        if abilities.Resurrection(7).get_effect():
            self.should_res = True

    def _get_damage_summary(self):
        dmg_summary = list()
        dmg = self.atk
        if self.first_attack:
            dmg += abilities.Backstab(8).get_effect()
            self.first_attack = False
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: dmg,
            constants.TARGET: constants.CARD_ACROSS
        }
        if self.lvl >= 5:
            dmg_summary.append(self._handle_lvl_5_ability())
        if not self.prevention:
            dmg_summary.append(for_dmg)
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
        if self.lvl == 10:
            return self._handle_lvl_10_ability()

    def exit_effect(self):
        if self.lvl == 10:
            return self._handle_lvl_10_ability(-1)

    def _handle_lvl_5_ability(self):
        self.receive_heal(abilities.Rejuvenation(4).get_effect())

    def _handle_lvl_10_ability(self, multiplier=1):
        forest_force = abilities.ForestForce(4)
        return [{
            constants.TARGET: forest_force.target,
            constants.EFFECT: multiplier * forest_force.get_effect()
        }]

    def _get_damage_summary(self):
        fireball = abilities.Fireball(3)
        dmg_summary = [{
            constants.EFFECT_TYPE: fireball.effect_type,
            constants.DAMAGE: fireball.get_effect(),
            constants.TARGET: fireball.target,
            constants.NUM_OF_TARGETS: fireball.num_of_targets,
        }]
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS
        }
        if not self.prevention:
            dmg_summary.append(for_dmg)
        if self.lvl >= 5:
            self._handle_lvl_5_ability()
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

    def _handle_lvl_5_ability(self):
        swamp_purity = abilities.SwampPurity(6)
        dmg2 = self.atk * (1 + swamp_purity.get_effect())
        return {
            constants.EFFECT_TYPE: swamp_purity.effect_type,
            constants.DAMAGE: (self.atk, dmg2),
            constants.TARGET: swamp_purity.target,
            constants.CONDITION: constants.CONDITION_TYPE,
            constants.CONDITION_PARAMETER: constants.SWAMP
        }

    def _handle_lvl_10_ability(self):
        chain_lightning = abilities.ChainLightning(6)
        return {
            constants.EFFECT_TYPE: chain_lightning.effect_type,
            constants.DAMAGE: chain_lightning.get_effect(),
            constants.TARGET: chain_lightning.target,
            constants.NUM_OF_TARGETS: chain_lightning.num_of_targets,
            constants.ATK_PREVENTION: chain_lightning.attack_prevention,
        }

    def _get_damage_summary(self):
        healing = abilities.Healing(6)
        dmg_summary = [{
            constants.EFFECT_TYPE: healing.effect_type,
            constants.HEAL: healing.get_effect(),
            constants.TARGET: healing.target
        }]
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS,
        }
        if self.lvl >= 5:
            for_dmg = self._handle_lvl_5_ability()
        if self.lvl == 10:
            dmg_summary.append(self._handle_lvl_10_ability())
        if not self.prevention:
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

    def _handle_lvl_5_ability(self):
        swamp_purity = abilities.SwampPurity(5)
        dmg2 = self.atk * (1 + swamp_purity.get_effect())
        return {
            constants.EFFECT_TYPE: swamp_purity.effect_type,
            constants.DAMAGE: (self.atk, dmg2),
            constants.TARGET: swamp_purity.target,
            constants.CONDITION: constants.CONDITION_TYPE,
            constants.CONDITION_PARAMETER: constants.SWAMP
        }

    def _handle_lvl_10_ability(self):
        snipe = abilities.Snipe(5)
        return {
            constants.EFFECT_TYPE: snipe.effect_type,
            constants.DAMAGE: snipe.get_effect(),
            constants.TARGET: snipe.target
        }

    def _get_damage_summary(self):
        snipe = abilities.Snipe(2)
        dmg_summary = [{
            constants.EFFECT_TYPE: snipe.effect_type,
            constants.DAMAGE: snipe.get_effect(),
            constants.TARGET: snipe.target
        }]
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS,
        }
        if self.lvl >= 5:
            for_dmg = self._handle_lvl_5_ability()
        if self.lvl == 10:
            dmg_summary.append(self._handle_lvl_10_ability())
        if not self.prevention:
            dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Wood Elf Archer - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)

    def __repr__(self):
        return 'Wood Elf Archer - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)
