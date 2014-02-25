import random

import constants


class Ability():
    ability_type = constants.DAMAGE
    occurs_once = False
    stacks = False
    num_of_targets = 1
    effect_type = constants.ATTACK
    target = constants.CARD_ACROSS

    def __init__(self, rank=None):
        self.rank = rank

    def get_effect(self):
        raise NotImplementedError('This ability needs an effect')


class Backstab(Ability):
    def get_effect(self):
        return 40 * self.rank


class ChainLightning(Ability):
    target = constants.ENEMY_RANDOM
    num_of_targets = 3
    attack_prevention = .4
    effect_type = constants.SPELL

    def get_effect(self):
        return 25 * self.rank


class Concentration(Ability):
    def get_effect(self):
        return (.2 * self.rank) * random.choice([0, 1])


class CounterAttack(Ability):
    def get_effect(self):
        return 30 * self.rank


class Curse(Ability):
    target = constants.ENEMY_HERO

    def get_effect(self):
        return 40 * self.rank


class Destroy(Ability):
    ability_type = constants.CARD_MANIPULATION
    effect_type = constants.DESTROY
    target = constants.ENEMY_RANDOM

    def get_effect(self):
        pass


class DevilsArmor(Ability):
    target = constants.CARD_ADJACENT
    num_of_targets = 3

    def get_effect(self):
        return 1500


class DevilsCurse(Ability):
    target = constants.ENEMY_HERO

    def get_effect(self):
        return 1000


class DevilsBlade(Ability):
    target = constants.CARD_LOWEST_HP

    def get_effect(self):
        return 2000


class Dodge(Ability):
    ability_type = constants.DAMAGE_MITIGATION
    target = constants.SELF

    def get_effect(self):
        base_dodge = .25
        dodge_inc = .05
        chance_to_dodge = base_dodge + dodge_inc * self.rank
        return chance_to_dodge > random.uniform(0, 1)


class Exile(Ability):
    ability_type = constants.CARD_MANIPULATION
    effect_type = constants.EXILE

    def get_effect(self):
        pass


class Fireball(Ability):
    target = constants.ENEMY_RANDOM
    effect_type = constants.SPELL

    def get_effect(self):
        low = 25 * self.rank
        high = 50 * self.rank
        return random.uniform(low, high)


class FireGod(Ability):
    target = constants.ALL_ENEMY_CARDS
    effect_type = constants.BURN

    def get_effect(self):
        return 20 * self.rank


class ForestForce(Ability):
    target = constants.OTHER_FOREST_ALLIES

    def get_effect(self):
        return 25 + self.rank


class Healing(Ability):
    ability_type = constants.HEAL
    target = constants.CARD_LOWEST_HP_ALLY
    effect_type = constants.HEAL

    def get_effect(self):
        return 25 * self.rank


class Immunity(Ability):
    ability_type = constants.DAMAGE_MITIGATION
    target = constants.SELF
    effect_type = constants.OTHER

    def get_effect(self):
        return constants.IMMUNE


class Laceration(Ability):
    ability_type = constants.CARD_MANIPULATION
    effect_type = constants.LACERATION

    def get_effect(self):
        pass


class Parry(Ability):
    ability_type = constants.DAMAGE_MITIGATION
    target = constants.SELF

    def get_effect(self):
        return 20 * self.rank


class Rejuvenation(Ability):
    ability_type = constants.HEAL
    target = constants.SELF
    effect_type = constants.HEAL

    def get_effect(self):
        return 30 * self.rank


class Resurrection(Ability):
    ability_type = constants.CARD_MANIPULATION
    target = constants.SELF
    effect_type = constants.OTHER

    def get_effect(self):
        return .30 + .05 * self.rank > random.uniform(0, 1)


class Retaliation(Ability):
    target = constants.CARD_ADJACENT
    num_of_targets = 3

    def get_effect(self):
        return 20 * self.rank


class Snipe(Ability):
    target = constants.CARD_LOWEST_HP
    effect_type = constants.PHYSICAL

    def get_effect(self):
        return 30 * self.rank


class SwampPurity(Ability):
    ability_type = constants.DAMAGE
    effect_type = constants.ATTACK_CONDITIONAL

    def get_effect(self):
        return .15 * (self.rank + 1)


class Thunderbolt(Ability):
    target = constants.ENEMY_RANDOM
    attack_prevention = .5
    effect_type = constants.SPELL

    def get_effect(self):
        return 25 * self.rank


class ToxicClouds(Ability):
    target = constants.ALL_ENEMY_CARDS
    effect_type = constants.SPELL

    def get_effect(self):
        return 20 * self.rank


class Trap(Ability):
    target = constants.ENEMY_MULTIPLE
    effect_type = constants.TRAP

    def get_effect(self):
        return self.rank
