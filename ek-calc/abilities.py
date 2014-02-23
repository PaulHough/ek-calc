import random

import constants


class Ability():
    def __init__(self, rank=None):
        self.rank = rank

    def get_effect(self):
        raise NotImplementedError('This ability needs an effect')


class Backstab(Ability):
    ability_type = constants.DAMAGE
    target = constants.SELF
    num_of_targets = 1
    effect_type = constants.ATTACK
    occurs_once = True
    stacks = False

    def get_effect(self):
        return 40 * self.rank


class Concentration(Ability):
    ability_type = constants.DAMAGE
    target = constants.ENEMY
    num_of_targets = 1
    effect_type = constants.ATTACK
    occurs_once = False
    stacks = False

    def get_effect(self):
        return (.2 * self.rank) * random.choice([0, 1])


class CounterAttack(Ability):
    ability_type = constants.DAMAGE
    target = constants.ENEMY
    num_of_targets = 1
    effect_type = constants.OTHER
    occurs_once = False
    stacks = False

    def get_effect(self):
        return 30 * self.rank


class DevilsCurse(Ability):
    ability_type = constants.DAMAGE
    target = constants.ENEMY_HERO
    num_of_targets = 1
    effect_type = constants.ATTACK
    occurs_once = False
    stacks = False

    def get_effect(self):
        return 1000


class DevilsBlade(Ability):
    ability_type = constants.DAMAGE
    target = constants.CARD_LOWEST_HP
    num_of_targets = 1
    effect_type = constants.ATTACK
    occurs_once = False
    stacks = False

    def get_effect(self):
        return 2000


class Dodge(Ability):
    ability_type = constants.DAMAGE_MITIGATION
    target = constants.SELF
    num_of_targets = 1
    effect_type = constants.ATTACK
    occurs_once = False
    stacks = False

    def get_effect(self):
        base_dodge = .25
        dodge_inc = .05
        chance_to_dodge = base_dodge + dodge_inc * self.rank
        return chance_to_dodge <= random.uniform(0, 1)


class Exile(Ability):
    ability_type = constants.CARD_MANIPULATION
    target = constants.CARD_ACROSS
    num_of_targets = 1
    effect_type = constants.EXILE
    occurs_once = False
    stacks = False

    def get_effect(self):
        pass


class Immunity(Ability):
    ability_type = constants.DAMAGE_MITIGATION
    target = constants.SELF
    num_of_targets = 1
    effect_type = constants.OTHER
    occurs_once = False
    stacks = False

    def get_effect(self):
        return constants.IMMUNE


class Laceration(Ability):
    ability_type = constants.CARD_MANIPULATION
    target = constants.ENEMY
    num_of_targets = 1
    effect_type = constants.OTHER
    occurs_once = False
    stacks = False

    def get_effect(self):
        return constants.NO_HEALS


class Retaliation(Ability):
    ability_type = constants.DAMAGE
    target = constants.CARD_ADJACENT
    num_of_targets = 3
    effect_type = constants.ATTACK
    occurs_once = False
    stacks = False

    def get_effect(self):
        return 20 * self.rank


class Snipe(Ability):
    ability_type = constants.DAMAGE
    target = constants.CARD_LOWEST_HP
    num_of_targets = 1
    effect_type = constants.ATTACK
    occurs_once = False
    stacks = False

    def get_effect(self):
        return 30 * self.rank


class SwampPurity(Ability):
    ability_type = constants.DAMAGE
    target = constants.CARD_ACROSS
    num_of_targets = 1
    effect_type = constants.ATTACK_CONDITIONAL
    occurs_once = False
    stacks = False

    def get_effect(self):
        return .15 * (self.rank + 1)
