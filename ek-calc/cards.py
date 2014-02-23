import abilities
import constants


class Card():
    effects = dict()

    def __init__(self, lvl=0):
        self.lvl = lvl
        self.hp = self._get_base_hp()
        self.atk = self._get_atk()

    def get_base_hp(self):
        return self._get_base_hp()

    def _get_base_hp(self):
        raise NotImplementedError('This card must have health.')

    def _get_atk(self):
        raise NotImplementedError('This card must have an attack.')

    def handle_abilities_offense(self):
        raise NotImplementedError('This card must have offensive abilities.')

    def handle_abilities_defense(self, dmg_summary):
        raise NotImplementedError('This card must have defensive abilities.')

    def is_dead(self):
        return self.hp <= 0

    def __str__(self):
        raise NotImplementedError(
            'Define how this card will display in results')

    def __repr__(self):
        raise NotImplementedError(
            'Define how this card will display in results')


class HeadlessHorseman(Card):
    card_type = constants.MOUNTAIN
    stars = 3
    wait = 2
    starting_wait = 2
    cost = 9
    first_attack = True

    def _get_base_hp(self):
        base_hp = 590
        hp_inc = 8
        return base_hp + hp_inc * self.lvl

    def _get_atk(self):
        base_atk = 165
        atk_inc = 29
        return base_atk + atk_inc * self.lvl

    def handle_abilities_defense(self, dmg_summary):
        self.hp -= abilities.Dodge(3).get_effect() * \
                   dmg_summary[constants.DAMAGE]
        reflect_summary = [
            {
                constants.EFFECT_TYPE: None,
                constants.DAMAGE: 0,
                constants.TARGET: None
            }
        ]
        return reflect_summary

    def handle_abilities_offense(self):
        dmg = self._get_atk()
        if self.lvl >= 5:
            if self.first_attack:
                dmg += abilities.Backstab(3).get_effect()
                self.first_attack = False
        if self.lvl == 10:
            dmg += self._get_atk()*abilities.Concentration(7).get_effect()
        dmg_summary = [{
            constants.EFFECT_TYPE: constants.ATTACK,
            constants.DAMAGE: dmg,
            constants.TARGET: constants.CARD_ACROSS
        }]

        return dmg_summary

    def __str__(self):
        return 'Headless Horseman - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)

    def __repr__(self):
        return 'Headless Horseman - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)


class WoodElfArcher(Card):
    card_type = constants.FOREST
    stars = 2
    wait = 2
    starting_wait = 2
    cost = 5

    def _get_base_hp(self):
        base_hp = 385
        hp_inc = 20
        return base_hp + hp_inc * self.lvl

    def _get_atk(self):
        base_atk = 105
        atk_inc = 24
        return base_atk + atk_inc * self.lvl

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
        dmg = self._get_atk()
        snipe = abilities.Snipe(2)
        dmg_summary = [{
            constants.EFFECT_TYPE: snipe.effect_type,
            constants.DAMAGE: snipe.get_effect(),
            constants.TARGET: snipe.target
        }]
        for_dmg = {
            constants.EFFECT_TYPE: constants.ATTACK,
            constants.DAMAGE: dmg,
            constants.TARGET: constants.CARD_ACROSS,
        }
        if self.lvl >= 5:
            swamp_purity = abilities.SwampPurity(5)
            dmg2 = dmg + self._get_atk() * swamp_purity.get_effect()
            for_dmg = {
                constants.EFFECT_TYPE: swamp_purity.effect_type,
                constants.DAMAGE: (dmg, dmg2),
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
        dmg_summary.append(for_dmg)
        return dmg_summary

    def __str__(self):
        return 'Wood Elf Archer - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)

    def __repr__(self):
        return 'Wood Elf Archer - Level: {}  HP: {}  ATK: {}'.\
            format(self.lvl, self.hp, self.atk)
