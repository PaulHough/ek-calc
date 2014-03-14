import abilities
import constants


class Rune():
    def __init__(self, lvl):
        if lvl < 0 or lvl > 4:
            raise ValueError('Runes must have a level 0 to 4.')
        self.lvl = lvl
        self.element = None
        self.stars = 0
        self.max_times = 0
        self.times_triggered = 0
        self.name = None

    def get_effect(self):
        raise NotImplementedError('Each rune must have an effect.')

    def get_triggering_conditions(self):
        raise NotImplementedError('Each rune must have a triggering condition')

    def __repr__(self):
        return self.__str__()


class Leaf(Rune):
    def __init__(self, lvl):
        super(Leaf, self).__init__(lvl=lvl)
        self.element = constants.AIR
        self.stars = 2
        self.max_times = 4
        self.name = constants.LEAF

    def get_triggering_conditions(self):
        return [{
            constants.TRIGGERING_CONDITION: constants.EXCEEDED_ROUNDS,
            constants.NUM_TO_ACTIVATE: 14,
        }]

    def get_effect(self):
        snipe = abilities.Snipe(self.lvl + 4)
        return [{
            constants.EFFECT_TYPE: snipe.effect_type,
            constants.TARGET: snipe.target,
            constants.DAMAGE: snipe.get_effect(),
        }]

    def __str__(self):
        return 'Leaf - Level: {}'.format(self.lvl)


class Revival(Rune):
    def __init__(self, lvl):
        super(Revival, self).__init__(lvl=lvl)
        self.element = constants.AIR
        self.stars = 3
        self.max_times = 4
        self.name = constants.REVIVAL

    def get_triggering_conditions(self):
        return [{
            constants.TRIGGERING_CONDITION: constants.CARD_IN_CEMETARY,
            constants.NUM_TO_ACTIVATE: 1,
            constants.CARD_TYPE: constants.FOREST
        }]

    def get_effect(self):
        group_morale = abilities.GroupMorale(self.lvl + 4)
        return [{
            constants.EFFECT_TYPE: group_morale.effect_type,
            constants.TARGET: group_morale.target,
            constants.EFFECT: group_morale.get_effect(),
        }]

    def __str__(self):
        return 'Revival - Level: {}'.format(self.lvl)


class Lore(Rune):
    def __init__(self, lvl):
        super(Lore, self).__init__(lvl=lvl)
        self.element = constants.FIRE
        self.stars = 5
        self.max_times = 4
        self.name = constants.LORE

    def get_triggering_conditions(self):
        return [{
            constants.TRIGGERING_CONDITION: constants.CARD_IN_CEMETARY,
            constants.NUM_TO_ACTIVATE: 2,
            constants.CARD_TYPE: constants.MOUNTAIN
        }]

    def get_effect(self):
        group_warpath = abilities.GroupWarpath(self.lvl + 6)
        return [{
            constants.EFFECT_TYPE: group_warpath.effect_type,
            constants.TARGET: group_warpath.target,
            constants.EFFECT: group_warpath.get_effect(),
        }]

    def __str__(self):
        return 'Lore - Level: {}'.format(self.lvl)


class FireForge(Rune):
    def __init__(self, lvl):
        super(FireForge, self).__init__(lvl=lvl)
        self.element = constants.FIRE
        self.stars = 3
        self.max_times = 4
        self.name = constants.FIREFORGE

    def get_triggering_conditions(self):
        return [{
            constants.TRIGGERING_CONDITION: constants.CARD_IN_CEMETARY,
            constants.NUM_TO_ACTIVATE: 1,
            constants.CARD_TYPE: constants.MOUNTAIN
        }]

    def get_effect(self):
        counterattack = abilities.GroupCounterAttack(self.lvl + 3)
        return [{
            constants.EFFECT_TYPE: counterattack.effect_type,
            constants.TARGET: counterattack.target,
            constants.EFFECT: counterattack.get_effect(),
        }]

    def __str__(self):
        return 'Fire Forge - Level: {}'.format(self.lvl)