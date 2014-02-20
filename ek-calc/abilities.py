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
        base_dmg = 40
        dmg_inc = 40
        return base_dmg + dmg_inc * self.rank


class Concentration(Ability):
    ability_type = constants.DAMAGE
    target = constants.ENEMY
    num_of_targets = 1
    effect_type = constants.ATTACK
    occurs_once = False
    stacks = False

    def get_effect(self):
        base_atk = .2
        atk_inc = .2
        return base_atk + atk_inc * self.rank


class DevilsCurse(Ability):
    ability_type = constants.DAMAGE
    target = constants.ENEMY_HERO
    num_of_targets = 1
    effect_type = constants.HP
    occurs_once = False
    stacks = False

    def get_effect(self):
        return 1000


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
        return base_dodge + dodge_inc * self.rank


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
    target = constants.ENEMY
    num_of_targets = 3
    effect_type = constants.ATTACK
    occurs_once = False
    stacks = False

    def get_effect(self):
        base_dmg = 20
        dmg_inc = 20
        return base_dmg + dmg_inc * self.rank
