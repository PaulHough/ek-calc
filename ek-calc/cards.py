import random

import abilities
import constants


class Card():
    def __init__(self, level=0, merit=False):
        if level > 10 or level < 0:
            raise ValueError('Cards must have a level within the range: 0 to 10')
        self.level = level
        self.hp = self._get_base_hp()
        self.atk = self._get_base_atk()
        self.should_res = False
        self.stunned = False
        self.prevention = False
        self.lacerate = False
        self.first_attack = True
        self.immune = False
        self.merit = merit
        self.effects = list()
        self.resistance = False

    def _get_base_hp(self):
        return self.base_hp + self.hp_inc * self.level

    def enter_effect(self):
        return list()

    def exit_effect(self):
        self.__init__(self.level, self.merit)
        return list()

    def _get_base_atk(self):
        return self.base_atk + self.atk_inc * self.level

    def resists_exile(self):
        return self.immune or self.resistance

    def resists_destroy(self):
        return self.immune or self.resistance

    def resists_teleportation(self):
        return self.immune or self.resistance

    def add_effect(self, dmg_summary):
        if self.immune:
            return
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

    def _handle_lvl_5_ability(self, *args, **kwargs):
        pass

    def _handle_lvl_10_ability(self, *args, **kwargs):
        pass

    def _get_damage_summary(self, *args, **kwargs):
        if self.prevention:
            return list()
        return [{
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS
        }]


    def handle_bloodthirsty(self):
        pass

    def handle_abilities_defense(self, dmg_summary):
        if not self.immune:
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

    def __str__(self, *args, **kwargs):
        raise NotImplementedError(
            'Define how this card will display in results')

    def __repr__(self):
        return self.__str__()


class Aranyani(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.FOREST
        self.stars = 5
        self.wait = 4
        self.starting_wait = 4
        self.cost = 14
        self.base_hp = 1350
        self.hp_inc = 36
        self.base_atk = 400
        self.atk_inc = 28
        super(Aranyani, self).__init__(*args, **kwargs)

    def enter_effect(self):
        if self.level == 10:
            return self._handle_lvl_10_ability()
        return list()

    def _handle_lvl_5_ability(self):
        healing = abilities.Healing(10)
        return [{
            constants.EFFECT_TYPE: healing.effect_type,
            constants.HEAL: healing.get_effect(),
            constants.TARGET: healing.target
        }]

    def _handle_lvl_10_ability(self):
        teleportation = abilities.Teleportation()
        return [{
            constants.EFFECT_TYPE: teleportation.effect_type,
            constants.TARGET: teleportation.target,
        }]

    def _get_reflect_summary(self, dmg_summary):
        if dmg_summary[constants.EFFECT_TYPE] in \
                constants.MAGIC_SHIELD_EFFECTS:
            dmg = 80
            if dmg_summary[constants.DAMAGE] < 80:
                dmg = dmg_summary[constants.DAMAGE]
            self.hp -= dmg
        else:
            self.hp -= dmg_summary.get(constants.DAMAGE)
        return list()

    def _get_damage_summary(self):
        dmg_summary = list()
        if self.level >= 5:
            dmg_summary = self._handle_lvl_5_ability()
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS
        }
        if not self.prevention:
            dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Aranyani - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class ArcticCephalid(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.TUNDRA
        self.stars = 5
        self.wait = 4
        self.starting_wait = 4
        self.cost = 16
        self.base_hp = 1200
        self.hp_inc = 30
        self.base_atk = 350
        self.atk_inc = 38
        super(ArcticCephalid, self).__init__(*args, **kwargs)

    def _get_reflect_summary(self, dmg_summary):
        if dmg_summary[constants.EFFECT_TYPE] in constants.SPELL:
            reflection = abilities.Reflection(7)
            return [{
                constants.EFFECT_TYPE: reflection.effect_type,
                constants.DAMAGE: reflection.get_effect(),
                constants.TARGET: reflection.target
            }]
        elif self.level >= 5 and \
                dmg_summary[constants.EFFECT_TYPE] is constants.ATK:
            dodge_chance = abilities.Dodge(8).get_effect()
            self.hp -= dodge_chance * dmg_summary.get(constants.DAMAGE, 0)
        else:
            self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        return list()

    def handle_bloodthirsty(self):
        if self.level == 10:
            bloodthirsty = abilities.Bloodthirsty(7)
            self.atk += bloodthirsty.get_effect()

    def __str__(self):
        return 'Arctic Cephalid - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class ArmoredMantis(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.FOREST
        self.stars = 3
        self.wait = 4
        self.starting_wait = 4
        self.cost = 9
        self.base_hp = 540
        self.hp_inc = 39
        self.base_atk = 125
        self.atk_inc = 18
        super(ArmoredMantis, self).__init__(*args, **kwargs)

    def _handle_lvl_10_ability(self):
        snipe = abilities.Snipe(7)
        return {
            constants.EFFECT_TYPE: snipe.effect_type,
            constants.DAMAGE: snipe.get_effect(),
            constants.TARGET: snipe.target
        }

    def _get_damage_summary(self):
        snipe = abilities.Snipe(3)
        dmg_summary = [{
            constants.EFFECT_TYPE: snipe.effect_type,
            constants.DAMAGE: snipe.get_effect(),
            constants.TARGET: snipe.target
        }]
        atk = self.atk
        if self.level >= 5:
            atk = self.atk * abilities.Concentration(5).get_effect()
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: atk,
            constants.TARGET: constants.CARD_ACROSS,
        }
        if self.level == 10:
            dmg_summary.append(self._handle_lvl_10_ability())
        if not self.prevention:
            dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Armored Mantis - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class Blackstone(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.MOUNTAIN
        self.stars = 4
        self.wait = 6
        self.starting_wait = 6
        self.cost = 14
        self.base_hp = 1250
        self.hp_inc = 26
        self.base_atk = 295
        self.atk_inc = 25
        super(Blackstone, self).__init__(*args, **kwargs)

    def _get_reflect_summary(self, dmg_summary):
        if self.level == 10 and \
                dmg_summary[constants.EFFECT_TYPE] in constants.SPELL:
            reflection = abilities.Reflection(5)
            return [{
                constants.EFFECT_TYPE: reflection.effect_type,
                constants.DAMAGE: reflection.get_effect(),
                constants.TARGET: reflection.target
            }]
        else:
            self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        return list()

    def _handle_lvl_5_ability(self):
        self.receive_heal(abilities.Rejuvenation(6).get_effect())

    def _get_damage_summary(self):
        if self.prevention:
            return list()
        if self.level >= 5:
            self._handle_lvl_5_ability()
        fire_god = abilities.FireGod(3)
        return [{
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
        return 'Blackstone - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class BloodWarrior(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.SWAMP
        self.stars = 4
        self.wait = 4
        self.starting_wait = 4
        self.cost = 13
        self.base_hp = 890
        self.hp_inc = 45
        self.base_atk = 250
        self.atk_inc = 24
        super(BloodWarrior, self).__init__(*args, **kwargs)

    def _get_reflect_summary(self, dmg_summary):
        if self.level >= 5 and \
                dmg_summary[constants.EFFECT_TYPE] in constants.SPELL:
            reflection = abilities.Reflection(4)
            return [{
                constants.EFFECT_TYPE: reflection.effect_type,
                constants.DAMAGE: reflection.get_effect(),
                constants.TARGET: reflection.target
            }]
        else:
            self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        return list()

    def handle_bloodthirsty(self):
        if self.level == 10:
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
        return 'Blood Warrior - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class BronzeDragon(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.FOREST
        self.stars = 4
        self.wait = 4
        self.starting_wait = 4
        self.cost = 13
        self.base_hp = 780
        self.hp_inc = 48
        self.base_atk = 200
        self.atk_inc = 20
        super(BronzeDragon, self).__init__(*args, **kwargs)

    def _get_reflect_summary(self, dmg_summary):
        if self.level == 10 and \
                dmg_summary[constants.EFFECT_TYPE] is constants.ATK:
            dodge_chance = abilities.Dodge(8).get_effect()
            self.hp -= dodge_chance * dmg_summary.get(constants.DAMAGE, 0)
        else:
            self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        return list()

    def _handle_lvl_5_ability(self):
        self.should_res = abilities.Resurrection(6).get_effect()

    def _get_damage_summary(self):
        thunderbolt = abilities.Thunderbolt(4)
        dmg_summary = [{
            constants.EFFECT_TYPE: thunderbolt.effect_type,
            constants.DAMAGE: thunderbolt.get_effect(),
            constants.TARGET: thunderbolt.target,
            constants.ATK_PREVENTION: thunderbolt.attack_prevention,
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
        return 'Bronze Dragon - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class CoiledDragon(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.TUNDRA
        self.stars = 4
        self.wait = 4
        self.starting_wait = 4
        self.cost = 12
        self.base_hp = 880
        self.hp_inc = 23
        self.base_atk = 235
        self.atk_inc = 28
        self.immune = False
        super(CoiledDragon, self).__init__(*args, **kwargs)

    def enter_effect(self):
        if self.level == 10:
            return self._handle_lvl_10_ability()
        return list()

    def exit_effect(self):
        super(CoiledDragon, self).exit_effect()
        if self.level == 10:
            return self._handle_lvl_10_ability(-1)
        return list()

    def _handle_lvl_10_ability(self, multiplier=1):
        northern_force = abilities.NorthernForce(5)
        return [{
            constants.TARGET: northern_force.target,
            constants.EFFECT: multiplier * northern_force.get_effect()
        }]

    def _get_reflect_summary(self, dmg_summary):
        if self.hp > 0 and dmg_summary[constants.EFFECT_TYPE] not in \
                constants.IMMUNITY_EFFECT_TYPES:
            if self.level >= 5:
                self.hp -= self._handle_lvl_5_ability(
                    dmg_summary[constants.DAMAGE])
        return list()

    def _handle_lvl_5_ability(self, dmg):
        parry = abilities.Parry(7)
        dmg_done = dmg - parry.get_effect()
        if dmg_done > 0:
            return dmg_done
        return 0

    def _get_damage_summary(self):
        dmg_summary = list()
        concentration = abilities.Concentration(5)
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk * concentration.get_effect(),
            constants.TARGET: constants.CARD_ACROSS
        }
        if not self.prevention:
            dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Coiled Dragon - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class DemonicImp(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.MOUNTAIN
        self.stars = 4
        self.wait = 4
        self.starting_wait = 4
        self.cost = 13
        self.base_hp = 850
        self.hp_inc = 15
        self.base_atk = 250
        self.atk_inc = 26
        super(DemonicImp, self).__init__(*args, **kwargs)
        self.resistance = True

    def _get_reflect_summary(self, dmg_summary):
        if self.level >= 5 and \
                dmg_summary[constants.EFFECT_TYPE] is constants.ATK:
            dodge_chance = abilities.Dodge(6).get_effect()
            self.hp -= dodge_chance * dmg_summary.get(constants.DAMAGE, 0)
        else:
            self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        return list()

    def _handle_lvl_10_ability(self):
        self.should_res = abilities.Resurrection(6).get_effect()

    def _get_damage_summary(self):
        dmg = self.atk
        if self.level >= 5:
            dmg += self.atk * abilities.Concentration(5).get_effect()
        dmg_summary = [{
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: dmg,
            constants.TARGET: constants.CARD_ACROSS
        }]
        if self.prevention:
            return list()
        return dmg_summary

    def __str__(self):
        return 'Demonic Imp - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class DireSnappingTurtle(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.MOUNTAIN
        self.stars = 5
        self.wait = 4
        self.starting_wait = 4
        self.cost = 15
        self.base_hp = 1300
        self.hp_inc = 40
        self.base_atk = 365
        self.atk_inc = 26
        super(DireSnappingTurtle, self).__init__(*args, **kwargs)

    def _handle_lvl_5_ability(self, *args, **kwargs):
        seal = abilities.Seal()
        return {
            constants.EFFECT_TYPE: seal.effect_type,
            constants.ATK_PREVENTION: seal.attack_prevention,
            constants.TARGET: seal.target
        }

    def _handle_lvl_10_ability(self, *args, **kwargs):
        bloodsucker = abilities.Bloodsucker(8)
        clean_sweep = abilities.CleanSweep()
        return [{
            constants.EFFECT_TYPE: bloodsucker.effect_type,
            constants.DAMAGE: self.atk,
            constants.TARGET: bloodsucker.target,
            constants.PERCENT_DAMAGE_DONE: bloodsucker.get_effect()
        }, {
            constants.EFFECT_TYPE: clean_sweep.effect_type,
            constants.DAMAGE: self.atk,
            constants.TARGET: clean_sweep.target
        }]

    def _get_damage_summary(self):
        clean_sweep = abilities.CleanSweep()
        dmg_summary = list()
        if self.level >= 5:
            dmg_summary.append(self._handle_lvl_5_ability())
        if not self.prevention:
            if self.level == 10:
                dmg_summary.extend(self._handle_lvl_10_ability())
            else:
                dmg_summary.append({
                    constants.EFFECT_TYPE: clean_sweep.effect_type,
                    constants.DAMAGE: self.atk,
                    constants.TARGET: clean_sweep.target
                })
        return dmg_summary

    def __str__(self):
        return 'Dire Snapping Turtle - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class FireKirin(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.FOREST
        self.stars = 5
        self.wait = 4
        self.starting_wait = 4
        self.cost = 14
        self.base_hp = 1300
        self.hp_inc = 26
        self.base_atk = 340
        self.atk_inc = 28
        super(FireKirin, self).__init__(*args, **kwargs)

    def _handle_lvl_5_ability(self):
        self.receive_heal(abilities.Rejuvenation(7).get_effect())

    def _handle_lvl_10_ability(self):
        self.should_res = abilities.Resurrection(7).get_effect()

    def _get_damage_summary(self):
        if self.level >= 5:
            self._handle_lvl_5_ability()
        fire_storm = abilities.FireStorm(8)
        dmg_summary = [{
            constants.EFFECT_TYPE: fire_storm.effect_type,
            constants.HEAL: fire_storm.get_effect(),
            constants.TARGET: fire_storm.target
        }]
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS,
        }
        if not self.prevention:
            dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Fire Kirin - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class FireDemon(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.MOUNTAIN
        self.stars = 5
        self.wait = 6
        self.starting_wait = 6
        self.cost = 14
        self.base_hp = 1350
        self.hp_inc = 36
        self.base_atk = 350
        self.atk_inc = 32
        super(FireDemon, self).__init__(*args, **kwargs)

        if self.level >= 10:
            self._handle_lvl_10_ability()

    def _get_reflect_summary(self, dmg_summary):
        if self.hp > 0 and dmg_summary[constants.EFFECT_TYPE] not in \
                constants.IMMUNITY_EFFECT_TYPES:
            self.hp -= dmg_summary[constants.DAMAGE]
        return list()

    def _handle_lvl_5_ability(self):
        laceration = abilities.Laceration()
        return {
            constants.EFFECT_TYPE: laceration.effect_type,
            constants.TARGET: laceration.target,
            constants.REMAINING: None
        }

    def _handle_lvl_10_ability(self):
        self.immune = True

    def _get_damage_summary(self):
        dmg = self.atk
        dmg += self.atk * abilities.Concentration(6).get_effect()
        dmg_summary = list()

        if self.level >= 5:
            dmg_summary.append(self._handle_lvl_5_ability())

        for_dmg = {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: dmg,
            constants.TARGET: constants.CARD_ACROSS
        }
        if not self.prevention:
            dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Fire Demon - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class GoblinCupid(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.SWAMP
        self.stars = 3
        self.wait = 2
        self.starting_wait = 2
        self.cost = 10
        self.base_hp = 640
        self.hp_inc = 27
        self.base_atk = 210
        self.atk_inc = 20
        super(GoblinCupid, self).__init__(*args, **kwargs)

        if self.level >= 5:
            self._handle_lvl_5_ability()

    def _get_reflect_summary(self, dmg_summary):
        if self.hp > 0 and \
                (self.resistance and dmg_summary[constants.EFFECT_TYPE] not in
                 constants.RESISTANCE_EFFECT_TYPES):
            if dmg_summary[constants.EFFECT_TYPE] is constants.ATK:
                self.hp -= self._handle_lvl_0_ability(dmg_summary[constants.DAMAGE])
        return list()

    def _handle_lvl_0_ability(self, dmg):
        parry = abilities.Parry(5)
        dmg_done = dmg - parry.get_effect()
        if dmg_done > 0:
            return dmg_done
        return 0

    def _handle_lvl_5_ability(self):
        self.resistance = True
        return

    def _get_damage_summary(self):
        dmg = self.atk
        if self.level >= 10:
            dmg += self.atk * abilities.Concentration(8).get_effect()
        dmg_summary = [{
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: dmg,
            constants.TARGET: constants.CARD_ACROSS
        }]
        if self.prevention:
            return list()
        return dmg_summary

    def __str__(self):
        return 'Goblin Cupid - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class HeadlessHorseman(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.MOUNTAIN
        self.stars = 3
        self.wait = 2
        self.starting_wait = 2
        self.cost = 9
        self.base_hp = 590
        self.hp_inc = 8
        self.base_atk = 165
        self.atk_inc = 29
        super(HeadlessHorseman, self).__init__(*args, **kwargs)

    def _get_reflect_summary(self, dmg_summary):
        if dmg_summary[constants.EFFECT_TYPE] is constants.ATK:
            dodge_chance = abilities.Dodge(3).get_effect()
            self.hp -= dodge_chance * dmg_summary.get(constants.DAMAGE, 0)
        else:
            self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        return list()

    def _get_damage_summary(self):
        if self.prevention:
            return list()
        dmg = self.atk
        if self.level >= 5:
            if self.first_attack:
                dmg += abilities.Backstab(3).get_effect()
                self.first_attack = False
        if self.level == 10:
            dmg += self.atk * abilities.Concentration(7).get_effect()
        dmg_summary = [{
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: dmg,
            constants.TARGET: constants.CARD_ACROSS
        }]
        return dmg_summary

    def __str__(self):
        return 'Headless Horseman - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class MossDragon(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.FOREST
        self.stars = 5
        self.wait = 6
        self.starting_wait = 6
        self.cost = 15
        self.base_hp = 1380
        self.hp_inc = 33
        self.base_atk = 355
        self.atk_inc = 30
        self.immune = True
        super(MossDragon, self).__init__(*args, **kwargs)

    def _get_reflect_summary(self, dmg_summary):
        if self.hp > 0 and dmg_summary[constants.EFFECT_TYPE] not in \
                constants.IMMUNITY_EFFECT_TYPES:
            if self.level >= 5:
                self.hp -= self._handle_lvl_5_ability(
                    dmg_summary[constants.DAMAGE])
        return list()

    def _handle_lvl_5_ability(self, dmg):
        parry = abilities.Parry(8)
        dmg_done = dmg - parry.get_effect()
        if dmg_done > 0:
            return dmg_done
        return 0

    def _get_damage_summary(self):
        dmg_summary = list()
        concentration = abilities.Concentration(6)
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk * concentration.get_effect(),
            constants.TARGET: constants.CARD_ACROSS
        }
        if not self.prevention:
            dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Moss Dragon - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class Necromancer(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.MOUNTAIN
        self.stars = 4
        self.wait = 4
        self.starting_wait = 4
        self.cost = 13
        self.base_hp = 720
        self.hp_inc = 25
        self.base_atk = 220
        self.atk_inc = 24
        super(Necromancer, self).__init__(*args, **kwargs)

    def _get_reflect_summary(self, dmg_summary):
        if self.level >= 5 and \
                dmg_summary[constants.EFFECT_TYPE] is constants.ATK:
            dodge_chance = abilities.Dodge(6).get_effect()
            self.hp -= dodge_chance * dmg_summary.get(constants.DAMAGE, 0)
        else:
            self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        return list()

    def _handle_lvl_10_ability(self):
        self.should_res = abilities.Resurrection(6).get_effect()

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
            format(self.level, self.hp, self.atk)


class PolarBearborn(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.TUNDRA
        self.stars = 4
        self.wait = 4
        self.starting_wait = 4
        self.cost = 12
        self.base_hp = 815
        self.hp_inc = 18
        self.base_atk = 260
        self.atk_inc = 30
        super(PolarBearborn, self).__init__(*args, **kwargs)

    def _get_reflect_summary(self, dmg_summary):
        if self.level == 10 and \
                dmg_summary[constants.EFFECT_TYPE] is constants.ATK:
            dodge_chance = abilities.Dodge(8).get_effect()
            self.hp -= dodge_chance * dmg_summary.get(constants.DAMAGE, 0)
        else:
            self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        return list()

    def _get_damage_summary(self):
        if self.prevention:
            return list()
        dmg = self.atk
        dmg += self.atk * abilities.Concentration(4).get_effect()
        if self.level >= 5:
            if self.first_attack:
                dmg += abilities.Backstab(5).get_effect()
                self.first_attack = False
        dmg_summary = [{
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: dmg,
            constants.TARGET: constants.CARD_ACROSS
        }]
        return dmg_summary

    def __str__(self):
        return 'Polar Bearborn - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class SkeletonKing(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.MOUNTAIN
        self.stars = 5
        self.wait = 2
        self.starting_wait = 2
        self.cost = 15
        self.base_hp = 1050
        self.hp_inc = 40
        self.base_atk = 225
        self.atk_inc = 40
        super(SkeletonKing, self).__init__(*args, **kwargs)

    def _get_reflect_summary(self, dmg_summary):
        self.hp -= dmg_summary.get(constants.DAMAGE, 0)
        if self.hp <= 0 and self.level == 10:
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
        self.should_res = abilities.Resurrection(7).get_effect()

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
        if self.level >= 5:
            dmg_summary.append(self._handle_lvl_5_ability())
        if not self.prevention:
            dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Skeleton King - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class SpitfireWorm(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.FOREST
        self.stars = 3
        self.wait = 4
        self.starting_wait = 4
        self.cost = 9
        self.base_hp = 600
        self.hp_inc = 17
        self.base_atk = 135
        self.atk_inc = 26
        super(SpitfireWorm, self).__init__(*args, **kwargs)

    def enter_effect(self):
        if self.level == 10:
            return self._handle_lvl_10_ability()
        return list()

    def exit_effect(self):
        super(SpitfireWorm, self).exit_effect()
        if self.level == 10:
            return self._handle_lvl_10_ability(-1)
        return list()

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
        if self.level >= 5:
            self._handle_lvl_5_ability()
        return dmg_summary

    def __str__(self):
        return 'Spitfire Worm - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class TaigaGeneral(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.TUNDRA
        self.stars = 5
        self.wait = 4
        self.starting_wait = 4
        self.cost = 15
        self.base_hp = 1320
        self.hp_inc = 43
        self.base_atk = 365
        self.atk_inc = 24
        super(TaigaGeneral, self).__init__(*args, **kwargs)

    def _handle_lvl_5_ability(self):
        exile = abilities.Exile()
        return [{
            constants.EFFECT_TYPE: exile.effect_type,
            constants.DAMAGE: 0,
            constants.TARGET: exile.target
        }]

    def _handle_lvl_10_ability(self):
        regeneration = abilities.Regeneration(7)
        return [{
            constants.EFFECT_TYPE: regeneration.effect_type,
            constants.TARGET: regeneration.target,
            constants.HEAL: regeneration.get_effect(),
        }]

    def _get_reflect_summary(self, dmg_summary):
        if dmg_summary[constants.EFFECT_TYPE] in \
                constants.MAGIC_SHIELD_EFFECTS:
            dmg = 80
            if dmg_summary[constants.DAMAGE] < 80:
                dmg = dmg_summary[constants.DAMAGE]
            self.hp -= dmg
        else:
            self.hp -= dmg_summary.get(constants.DAMAGE)
        return list()

    def _get_damage_summary(self):
        dmg_summary = list()
        if self.level >= 5:
            dmg_summary = self._handle_lvl_5_ability()
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATK,
            constants.DAMAGE: self.atk,
            constants.TARGET: constants.CARD_ACROSS
        }
        if not self.prevention:
            dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Taiga General - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class Troglodyte(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.FOREST
        self.stars = 3
        self.wait = 4
        self.starting_wait = 4
        self.cost = 9
        self.base_hp = 680
        self.hp_inc = 28
        self.base_atk = 180
        self.atk_inc = 23
        super(Troglodyte, self).__init__(*args, **kwargs)

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
        if self.level >= 5:
            for_dmg = self._handle_lvl_5_ability()
        if self.level == 10:
            dmg_summary.append(self._handle_lvl_10_ability())
        if not self.prevention:
            dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Troglodyte - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)


class WoodElfArcher(Card):
    def __init__(self, *args, **kwargs):
        self.card_type = constants.FOREST
        self.stars = 2
        self.wait = 2
        self.starting_wait = 2
        self.cost = 5
        self.base_hp = 385
        self.hp_inc = 20
        self.base_atk = 105
        self.atk_inc = 24
        super(WoodElfArcher, self).__init__(*args, **kwargs)

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
        if self.level >= 5:
            for_dmg = self._handle_lvl_5_ability()
        if self.level == 10:
            dmg_summary.append(self._handle_lvl_10_ability())
        if not self.prevention:
            dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Wood Elf Archer - Level: {}  HP: {}  ATK: {}'.\
            format(self.level, self.hp, self.atk)
