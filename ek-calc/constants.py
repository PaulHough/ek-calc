
NO_REFLECTED_DAMAGE = 0

AIR = 'air'
ALL_ALLY_CARDS = 'all_ally_cards'
ALL_ENEMY_CARDS = 'all_enemy_cards'
ATK_BUFF = 'atk_buff'
ATK_PERCENTBUFF = 'atk_percentbuff'
ATK = 'atk'
ATK_COND = 'atk_cond'
ATK_PREVENTION = 'atk_prevention'
BITE = 'bite'
BLOOD = 'blood'
BLOODSUCKER = 'bloodsucker'
BLOODTHIRSTY = 'bloodthirsty'
BURN = 'burn'
CARD_ACROSS = 'card_across'
CARD_ADJACENT = 'card_adjacent'
CARD_IN_CEMETERY = 'card_in_cemetery'
CARD_LOWEST_HP = 'card_lowest_hp'
CARD_LOWEST_HP_ALLY = 'card_lowest_hp_ally'
CARD_MANIPULATION = 'card_manipulation'
CARD_TYPE = 'card_type'
CONDITION = 'condition'
CONDITION_TYPE = 'condition_type'
CONDITION_PARAMETER = 'condition_parameter'
DAMAGE_MITIGATION = 'damage_mitigation'
DAMAGE = 'damage'
DEMON = 'demon'
DESTROY = 'destroy'
EFFECT = 'effect'
EFFECT_TYPE = 'effect_type'
ENEMY = 'enemy'
ENEMY_HERO = 'enemy_hero'
ENEMY_MULTIPLE = 'enemy_multiple'
ENEMY_RANDOM = 'enemy_random'
EXCEEDED_ROUNDS = 'exceeded_rounds'
EXILE = 'exile'
EXTRA_EFFECT = 'extra_effect'
FIRE = 'fire'
FIREFORGE = 'fire_forge'
FOREST = 'forest'
HEAL = 'heal'
HP = 'hp'
ICE = 'ice'
IMMUNE = 'immune'
LACERATION = 'laceration'
LEAF = 'leaf'
LIGHTNING = 'lightning'
LONGEST_WAIT_TIME = 'longest_wait_time'
LORE = 'lore'
MOUNTAIN = 'mountain'
NO_HEALS = 'no_heals'
NUM_OF_TARGETS = 'num_of_targets'
NUM_TO_ACTIVATE = 'num_to_activate'
OTHER = 'other'
OTHER_FOREST_ALLIES = 'other_forest_allies'
OTHER_TUNDRA_ALLIES = 'other_tundra_allies'
PHYSICAL = 'physical'
PERCENT_DAMAGE_DONE = 'percent_damage_done'
PLAGUE = 'plague'
POISON = 'poison'
REMAINING = 'remaining'
RESURRECTION = 'resurrection'
RESISTANCE = 'resistance'
REVIVAL = 'revival'
SACRIFICE = 'sacrifice'
SEAL = 'seal'
SELF = 'self'
SMOG = 'smog'
STUN = 'stun'
SWAMP = 'swamp'
TARGET = 'target'
TELEPORTATION = 'teleportation'
TRIGGERING_CONDITION = 'triggering_condition'
TUNDRA = 'tundra'
TURN = 'turn'
TRAP = 'trap'
VENOM = 'venom'

IMMUNITY_EFFECT_TYPES = (
    ICE, LIGHTNING, TRAP, SEAL, SACRIFICE, EXILE, DESTROY, LACERATION, FIRE
)

RESISTANCE_EFFECT_TYPES = (
    EXILE, DESTROY, TELEPORTATION
)

SPELL = (ICE, LIGHTNING, FIRE, BLOOD)
DAMAGE_TO_HERO_EFFECT_TYPES = (ATK, ENEMY_HERO)
PERSISTENT_EFFECTS = (BURN, SMOG, POISON, VENOM, SEAL)
STUN_TYPES = (TRAP, STUN)
CAN_DAMAGE_PLAYER = (ATK, ATK_COND)
MAGIC_SHIELD_EFFECTS = (FIRE, ICE, LIGHTNING, BLOOD)
