from models import Skill, SavingThrow, SpecialAbility, Sense, Language, DamageResistance, DamageImmunity, DamageVulnerability, ConditionImmunity, Action
from create_nested_monster_routes_test import create_nested_monster_routes_test

TestSkillRoutes = create_nested_monster_routes_test(
    "skills", 
    Skill, 
    { "name": "history", "value": 2 }, 
    { "name": "arcana", "value": 10 }
)

TestSavingThrowRoutes = create_nested_monster_routes_test(
    "saving_throws", 
    SavingThrow, 
    { "name": "dex", "value": 2 }, 
    { "name": "str", "value": 5 }
)

TestSpecialAbilityRoutes = create_nested_monster_routes_test(
    "special_abilities", 
    SpecialAbility, 
    { "name": "Amphibious", "description": "Able to breathe air and water" }, 
    { "name": "Devil's Sight", "description": "Able to see even in magical darkness" }
)

TestSenseRoutes = create_nested_monster_routes_test(
    "senses", 
    Sense, 
    { "name": "darkvision", "distance": 60 }, 
    { "name": "blindsight", "distance": 10 }
)

TestLanguageRoutes = create_nested_monster_routes_test(
    "languages", 
    Language, 
    { "name": "sylvan" }, 
    { "name": "infernal" }
)

TestLanguageRoutes = create_nested_monster_routes_test(
    "languages", 
    Language, 
    { "name": "sylvan" }, 
    { "name": "infernal" }
)

TestDamageResistanceRoutes = create_nested_monster_routes_test(
    "damage_resistances", 
    DamageResistance, 
    { "damage_type": "fire" }, 
    { "damage_type": "cold" }
)

TestDamageImmunityRoutes = create_nested_monster_routes_test(
    "damage_immunities", 
    DamageImmunity, 
    { "damage_type": "poison" }, 
    { "damage_type": "psychic" }
)

TestDamageVulnerabilityRoutes = create_nested_monster_routes_test(
    "damage_vulnerabilities", 
    DamageVulnerability, 
    { "damage_type": "thunder" }, 
    { "damage_type": "lightning" }
)

TestConditionImmunityRoutes = create_nested_monster_routes_test(
    "condition_immunities", 
    ConditionImmunity, 
    { "condition_type": "prone" }, 
    { "condition_type": "poisoned" }
)

TestActionRoutes = create_nested_monster_routes_test(
    "actions", 
    Action, 
    { "name": "Stabby Stab", "description": "Stabs something a bunch" }, 
    { "name": "Slash slash", "description": "Slashes something a bunch" }
)