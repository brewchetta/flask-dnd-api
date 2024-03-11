from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
from damage_types import DAMAGE_TYPES

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# MONSTER #############################################
# Relationships:
#     many skills
#     many saving_throws
#     many special_abilities
#     many senses
#     many languages
#     many actions
#     many spells through monster_spells
# ####################################################

class Monster(db.Model, SerializerMixin):

    CATEGORIES = ["aberration", "beast", "celestial", "construct", "dragon", "elemental", "fey", "fiend", "giant", "humanoid", "monstrosity", "ooze", "plant", "undead"]

    __tablename__ = "monsters_table"

    # COLUMNS #

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String, nullable=False)
    size = db.Column(db.String, default="medium")
    alignment = db.Column(db.String)

    category = db.Column(db.String)
    sub_category = db.Column(db.String)

    armor_class = db.Column(db.Integer, default=10)
    hit_points = db.Column(db.Integer, default=1)
    hit_dice_count = db.Column(db.Integer, default=1)
    hit_dice_size = db.Column(db.Integer, default=10)

    strength = db.Column(db.Integer, default=10)
    dexterity = db.Column(db.Integer, default=10)
    constitution = db.Column(db.Integer, default=10)
    intelligence = db.Column(db.Integer, default=10)
    wisdom = db.Column(db.Integer, default=10)
    charisma = db.Column(db.Integer, default=10)

    passive_perception = db.Column(db.Integer, default=10)

    challenge_rating = db.Column(db.Integer, default=0)
    proficiency_bonus = db.Column(db.Integer, default=2)

    spellcasting_level = db.Column(db.Integer, default=0)
    spellcasting_ability = db.Column(db.String)
    spell_save_dc = db.Column(db.Integer, default=0)
    spell_modifier = db.Column(db.Integer, default=0)

    spell_slots_first_level = db.Column(db.Integer, default=0)
    spell_slots_second_level = db.Column(db.Integer, default=0)
    spell_slots_third_level = db.Column(db.Integer, default=0)
    spell_slots_fourth_level = db.Column(db.Integer, default=0)
    spell_slots_fifth_level = db.Column(db.Integer, default=0)
    spell_slots_sixth_level = db.Column(db.Integer, default=0)
    spell_slots_seventh_level = db.Column(db.Integer, default=0)
    spell_slots_eighth_level = db.Column(db.Integer, default=0)
    spell_slots_ninth_level = db.Column(db.Integer, default=0)

    # SERIALIZER #

    serialize_rules = ("-skills.monster", "-saving_throws.monster", "-special_abilities.monster", "-senses.monster", "-speeds.monster", "-languages.monster", "-damage_resistances.monster", "-damage_immunities.monster", "-damage_vulnerabilities.monster", "-condition_immunities.monster", "-actions.monster", "-monster_spells", "spells", "-spells.monster_spells")

    # VALIDATIONS #

    @validates("category")
    def validate_category(self, k, v):
        if v.lower() in self.CATEGORIES:
            return v.lower()
        raise ValueError(f"{k} must be a valid monster category ('aberration', 'beast', 'celestial', 'construct', 'dragon', 'elemental', 'fey', 'fiend', 'giant', 'humanoid', 'monstrosity', 'ooze', 'plant', 'undead') but you put {v}")

    @validates("strength", "dexterity", "intelligence", "constitution", "wisdom", "charisma")
    def validate_ability_scores(self, k, v):
        if 0 <= v <= 30:
            return v
        raise ValueError(f"{k} must be between 0 and 30 inclusive but received {v}")

    @validates("armor_class", "hit_points", "hit_dice_count", "challenge_rating", "proficiency_bonus")
    def validate_non_zero_stats(self, k, v):
        if int(v) >= 0:
            return v
        raise ValueError(f"{k} must be 1 or greater but received {v}")
    
    @validates("hit_dice_size")
    def validate_dice_values(self, k, v):
        if v in [ 4, 6, 8, 10, 12 ]:
            return v
        raise ValueError(f"{k} must be a valid size (4, 6, 8, 10, 12) but received {v}")
    
    @validates("spell_slots_first_level", "spell_slots_second_level", "spell_slots_third_level", "spell_slots_fourth_level", "spell_slots_fifth_level", "spell_slots_sixth_level", "spell_slots_seventh_level", "spell_slots_eighth_level", "spell_slots_ninth_level")
    def validate_spell_slots_sizes(self, k, v):
        if v in [0,1,2,3,4]:
            return v
        raise ValueError(f"{k} must be a valid size (0-4) but received {v}")
    
    # RELATIONSHIPS #

    skills = db.relationship("Skill", back_populates="monster")

    saving_throws = db.relationship("SavingThrow", back_populates="monster")

    special_abilities = db.relationship("SpecialAbility", back_populates="monster")

    senses = db.relationship("Sense", back_populates="monster")

    speeds = db.relationship("Speed", back_populates="monster")

    languages = db.relationship("Language", back_populates="monster")

    damage_resistances = db.relationship("DamageResistance", back_populates="monster")
    damage_immunities = db.relationship("DamageImmunity", back_populates="monster")
    damage_vulnerabilities = db.relationship("DamageVulnerability", back_populates="monster")
    condition_immunities = db.relationship("ConditionImmunity", back_populates="monster")

    actions = db.relationship("Action", back_populates="monster")

    monster_spells = db.relationship("MonsterSpell", back_populates="monster")
    spells = association_proxy("monster_spells", "spell")

# END Monster #


# CHARACTER SKILL #####################################
# Example: Skill(value="2", name="history")
# ####################################################

class Skill(db.Model, SerializerMixin):
    SKILLS = ['acrobatics', 'animal handling', 'arcana', 'athletics', 'deception', 'history', 'insight', 'intimidation', 'investigation', 'medicine', 'nature', 'perception', 'performance', 'persuasion', 'religion', 'sleight of hand', 'stealth', 'survival']
    
    __tablename__ = "skills_table"

    # COLUMNS #

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, default=0)
    name = db.Column(db.String, nullable=False)

    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
    monster = db.relationship("Monster", back_populates="skills")

    # SERIALIZER #

    serialize_rules = ("-monster",)

    # VALIDATIONS #

    @validates('name')
    def validate_skill_name(self, k, v):
        if v.lower().strip() in self.SKILLS:
            return v.lower().strip()
        raise ValueError(f"{k} must be a valid skill name ({ ', '.join(self.SKILLS) }) but got {v}")
    
# END Skill #
    

# # CHARACTER SAVING THROW ##############################
# # Example: SavingThrow(value="2", name="dex")
# # Example: SavingThrow(value="2", name="dexterity")
# # ####################################################

class SavingThrow(db.Model, SerializerMixin):
    ABILITIES = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma', 'str', 'dex', 'con', 'wis', 'int', 'cha']
    ABILITIES_DICT = { 'strength': 'str', 'dexterity': 'dex', 'constitution': 'con', 'wisdom': 'wis', 'intelligence': 'int', 'charisma': 'cha' }

    __tablename__ = "saving_throws_table"

    # COLUMNS #

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    value = db.Column(db.Integer)

    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
    monster = db.relationship("Monster", back_populates="saving_throws")

    # SERIALIZER #

    serialize_rules = ("-monster",)

    # VALIDATIONS #

    # name ######################################
    # must be within ABILITIES and converted to 
    # 3 letter signifier with ABILITIES_DICT
    # ##########################################
    @validates('name')
    def validate_skill_name(self, k, v):
        if v.lower().strip() in self.ABILITIES:
            return self.ABILITIES_DICT.get(v.lower()) or v.lower().strip()
        raise ValueError(f"{k} must be a valid saving throw name ({ ', '.join(self.ABILITIES) }) but got {v}")

# END SavingThrow #


# # CHARACTER SPECIAL ABILITY ###########################
# # Example: SpecialAbility(name="Amphibious", 
# # description="The Aboleth can breath water and air")
# # 
# # belongs to monster
# # ####################################################

class SpecialAbility(db.Model, SerializerMixin):
    __tablename__ = "special_abilities_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
    monster = db.relationship("Monster", back_populates="special_abilities")

    serialize_rules = ("-monster",)
    
# END SpecialAbility #


# # CHARACTER SENSE #####################################
# # Example: Sense(name="darkvision", distance=120)
# # ####################################################

class Sense(db.Model, SerializerMixin):
    __tablename__ = "senses_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    distance = db.Column(db.Integer)
    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
    monster = db.relationship("Monster", back_populates="senses")

    serialize_rules = ("-monster",)
    
# END Sense #


# # CHARACTER SPEED #####################################
# # Example: Speed(name="walk", distance="20 ft.")
# # ####################################################

class Speed(db.Model, SerializerMixin):
    __tablename__ = "speed_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    distance = db.Column(db.Integer)
    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
    monster = db.relationship("Monster", back_populates="speeds")

    serialize_rules = ("-monster",)
    
# END Speed #


# # CHARACTER LANGUAGE ##################################
# # Example: Language(name="deep speech")
# # ####################################################

class Language(db.Model, SerializerMixin):
    __tablename__ = "languages_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
    monster = db.relationship("Monster", back_populates="languages")

    serialize_rules = ("-monster",)

# END Language #


# # DAMAGE MODEL #########################################
# # Example: DamageResistance(name="cold")
# # 
# # DamageResistance, DamageImmunity, DamageVulnerability 
# # all require valid damage type
# # ####################################################

class DamageResistance(db.Model, SerializerMixin):
    DAMAGE_TYPES = DAMAGE_TYPES

    __tablename__ = "damage_resistances_table"

    id = db.Column(db.Integer, primary_key=True)
    
    damage_type = db.Column(db.String, nullable=False)
    
    monster = db.relationship("Monster", back_populates="damage_resistances")
    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))

    @validates("damage_type")
    def validate_damage_type(self, k, v):
        if v.lower().strip() in self.DAMAGE_TYPES:
            return v.lower().strip()
        raise ValueError(f"{k} must be a valid damage type ({ ', '.join(self.DAMAGE_TYPES) }) but got {v}")

    serialize_rules = ("-monster",)

class DamageImmunity(db.Model, SerializerMixin):
    DAMAGE_TYPES = DAMAGE_TYPES
    __tablename__ = "damage_immunities_table"

    id = db.Column(db.Integer, primary_key=True)

    damage_type = db.Column(db.String, nullable=False)

    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
    monster = db.relationship("Monster", back_populates="damage_immunities")


    @validates("damage_type")
    def validate_damage_type(self, k, v):
        if v.lower().strip() in self.DAMAGE_TYPES:
            return v.lower().strip()
        raise ValueError(f"{k} must be a valid damage type ({ ', '.join(self.DAMAGE_TYPES) }) but got {v}")

    serialize_rules = ("-monster",)

class DamageVulnerability(db.Model, SerializerMixin):
    DAMAGE_TYPES = DAMAGE_TYPES
    __tablename__ = "damage_vulnerabilities_table"

    id = db.Column(db.Integer, primary_key=True)
    
    damage_type = db.Column(db.String, nullable=False)
    
    monster = db.relationship("Monster", back_populates="damage_vulnerabilities")
    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))

    @validates("damage_type")
    def validate_damage_type(self, k, v):
        if v.lower().strip() in self.DAMAGE_TYPES:
            return v.lower().strip()
        raise ValueError(f"{k} must be a valid damage type ({ ', '.join(self.DAMAGE_TYPES) }) but got {v}")

    serialize_rules = ("-monster",)

# END DamageModels #

    
# # CONDITION IMMUNITY ######################################
# # Example: ConditionImmunity(name="charmed")
# # ####################################################

class ConditionImmunity(db.Model, SerializerMixin):
    CONDITION_TYPES = ['blinded', 'charmed', 'deafened', 'exhaustion', 'frightened', 'grappled', 'incapacitated', 'invisible', 'paralyzed', 'petrified', 'poisoned', 'prone', 'restrained', 'stunned', 'unconscious']
    __tablename__ = "condition_immunities_table"

    id = db.Column(db.Integer, primary_key=True)
    condition_type = db.Column(db.String, nullable=False)
    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
    monster = db.relationship("Monster", back_populates="condition_immunities")

    serialize_rules = ("-monster",)

    @validates("condition_type")
    def validate_condition_type(self, k, v):
        if v.lower().strip() in self.CONDITION_TYPES:
            return v.lower().strip()
        raise ValueError(f"{k} must be a valid condition type ({ ', '.join(self.CONDITION_TYPES) }) but got {v}")
    
# END ConditionImmunity #


# # CHARACTER ACTION ####################################
# # Example: Action(name="Club", description="Melee Weapon 
# # Attack: +2 to hit, reach 5ft., one target. Hit: 2 (1d4) 
# # bludgeoning damage.")
# # 
# # Actions belong to one monster
# # ####################################################

class Action(db.Model, SerializerMixin):
    __tablename__ = "actions_table"

    id = db.Column(db.Integer, primary_key=True)
    legendary_action = db.Column(db.Boolean, default=False)
    lair_action = db.Column(db.Boolean, default=False)
    name = db.Column(db.String)
    description = db.Column(db.String, nullable=False)
    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
    monster = db.relationship("Monster", back_populates="actions")

    serialize_rules = ("-monster",)
    
# END Action #


# # CHARACTER SPELL #####################################
# # Example: Spell()
# # 
# # MonsterSpell exists only as a join table
# # ####################################################

class Spell(db.Model, SerializerMixin):
    SPELL_SCHOOLS = ['abjuration', 'conjuration', 'divination', 'enchantment', 'evocation', 'illusion', 'necromancy', 'transmutation', 'dunamancy']

    __tablename__ = "spells_table"

    # COLUMNS #

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    level = db.Column(db.Integer, default=0)
    casting_time = db.Column(db.String)
    duration = db.Column(db.String)
    range_area = db.Column(db.String)
    at_higher_levels = db.Column(db.String)
    
    verbal = db.Column(db.Boolean, default=False)
    somatic = db.Column(db.Boolean, default=False)
    material = db.Column(db.String)

    school = db.Column(db.String)
    attack_save = db.Column(db.String)
    damage_effect = db.Column(db.String)

    # RELATIONSHIPS #

    monster_spells = db.relationship("MonsterSpell", back_populates="spell")

    # SERIALIZER #

    serialize_rules = ("-monster_spells",)

    # VALIDATIONS #

    # @validates('damage_type')
    # def validate_damage_type(self, k, v):
    #     if v == '' or v == None:
    #         return None
    #     if v.lower().strip() in self.DAMAGE_TYPES:
    #         return v.lower().strip()
    #     raise ValueError(f"{k} must be a valid damage type ({ ', '.join(self.DAMAGE_TYPES) }) or a null value but got {v}")

    @validates('school')
    def validate_school(self, k, v):
        if v.lower().strip() in self.SPELL_SCHOOLS:
            return v.lower().strip()
        raise ValueError(f"{k} must be a valid magic school ({ ', '.join(self.SPELL_SCHOOLS) }) but got {v}")

# END Spell #


class MonsterSpell(db.Model, SerializerMixin):
    __tablename__ = "monster_spells_table"

    id = db.Column(db.Integer, primary_key=True)

    spell_id = db.Column(db.Integer, db.ForeignKey("spells_table.id"))
    spell = db.relationship("Spell", back_populates="monster_spells")

    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
    monster = db.relationship("Monster", back_populates="monster_spells")

    serialize_rules = ("-monster",)

# END MonsterSpell #
    
# TODO: Build Speed model for monster speeds