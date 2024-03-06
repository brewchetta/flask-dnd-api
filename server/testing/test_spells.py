SPELL_ONE = {
    "name": "Acid Arrow",

    "description": "A shimmering green arrow streaks toward a target within range and bursts in a spray of acid. Make a ranged spell attack against the target. On a hit, the target takes 4d4 acid damage immediately and 2d4 acid damage at the end of its next turn. On a miss, the arrow splashes the target with acid for half as much of the initial damage and no damage at the end of its next turn.",

    "level": 2,
    "casting_time": "1 Action",
    "duration": "Instantaneous",
    "range_area": "90 ft",

    "at_higher_levels": "When you cast this spell using a spell slot of 3rd level or higher, the damage (both initial and later) increases by 1d4 for each slot level above 2nd.",

    "verbal": True,
    "somatic": True,
    "material": "powdered rhubarb leaf and an adder's stomach",

    "school": "evocation",
    "attack_save": "Ranged",
    "damage_type": "acid"
}

SPELL_TWO = {
    "name": "Aid",

    "description": "Your spell bolsters your allies with toughness and resolve. Choose up to three creatures within range. Each target's hit point maximum and current hit points increase by 5 for the duration.",

    "level": 2,
    "casting_time": "1 Action",
    "duration": "8 Hours",
    "range_area": "30 ft",

    "at_higher_levels": "When you cast this spell using a spell slot of 3rd level or higher, a target's hit points increase by an additional 5 for each slot level above 2nd.",

    "verbal": True,
    "somatic": True,
    "material": "a tiny strip of white cloth",

    "school": "abjuration"
}

SPELL_THREE = {
    "name": "Control Flames",

    "description": "You choose nonmagical flame that you can see within range and that fits within a 5-foot cube. You affect it in one of the following ways:\n\nYou instantaneously expand the flame 5 feet in one direction, provided that wood or other fuel is present in the new location.\nYou instantaneously extinguish the flames within the cube.\nYou double or halve the area of bright light and dim light cast by the flame, change its color, or both. The change lasts for 1 hour.\nYou cause simple shapes—such as the vague form of a creature, an inanimate object, or a location—to appear within the flames and animate as you like. The shapes last for 1 hour.\n\nIf you cast this spell multiple times, you can have up to three of its non-instantaneous effects active at a time, and you can dismiss such an effect as an action.",

    "level": 0,
    "casting_time": "1 Action",
    "duration": "Instantaneous",
    "range_area": "60 ft / 5 ft cube",

    "somatic": True,

    "school": "transmutation",
    "effect_type": "control"
}

SPELL_FOUR = {
    "name": "Mage Hand",

    "description": "A spectral, floating hand appears at a point you choose within range. The hand lasts for the duration or until you dismiss it as an action. The hand vanishes if it is ever more than 30 feet away from you or if you cast this spell again.\n\nYou can use your action to control the hand. You can use the hand to manipulate an object, open an unlocked door or container, stow or retrieve an item from an open container, or pour the contents out of a vial. You can move the hand up to 30 feet each time you use it.\n\nThe hand can't attack, activate magic items, or carry more than 10 pounds.",

    "level": 0,
    "casting_time": "1 Action",
    "duration": "1 Minute",
    "range_area": "30 ft",

    "somatic": True,
    "verbal": True,

    "school": "conjuration",
    "effect_type": "utility"
}