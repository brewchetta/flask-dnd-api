from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

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
        if v > 0:
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

# END Monster #


# CHARACTER SKILL #####################################
# Example: Skill(value="2", name="history")
# ####################################################

class Skill(db.Model, SerializerMixin):
    SKILLS = ['acrobatics', 'animal handling', 'arcana', 'athletics', 'deception', 'history', 'insight', 'intimidation', 'investigation', 'medicine', 'nature', 'perception', 'performance', 'persuasion', 'religion', 'sleight of hand', 'stealth', 'survival']
    
    __tablename__ = "skills_table"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, default=0)
    name = db.Column(db.String, nullable=False)

    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
    monster = db.relationship("Monster", back_populates="skills")

    @validates('name')
    def validate_skill_name(self, k, v):
        if v.lower() in self.SKILLS:
            return v.lower()
        raise ValueError(f"{k} must be a valid skill name ({ ', '.join(self.SKILLS) }) but got {v}")
    
# # CHARACTER SAVING THROW ##############################
# # Example: SavingThrow(value="2", name="dex")
# # Example: SavingThrow(value="2", name="dexterity")
# # ####################################################

# class SavingThrow(db.Model, SerializerMixin):
#     __tablename__ = "saving_throws_table"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     value = db.Column(db.String)

#     monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
#     monster = db.relationship("Monster", back_populates="skill_values")

# # TODO: Add validations for saving throws names
# # TODO: Saving throw names get shorted to attribute name on validation
# # TODO: Add association on Monster
    

# # CHARACTER SPECIAL ABILITY ###########################
# # Example: SpecialAbility(name="Amphibious", 
# # description="The Aboleth can breath water and air")
# # 
# # belongs to monster
# # ####################################################

# class SpecialAbility(db.Model, SerializerMixin):
#     __tablename__ = "special_abilities_table"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     description = db.Column(db.String, nullable=False)

#     monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
#     monster = db.relationship("Monster", back_populates="skill_values")
# # TODO: Add association on Monster


# # CHARACTER SENSE #####################################
# # Example: Sense(name="darkvision", distance=120)
# # 
# # Example: Sense(name="passive perception", passive_score=12)
# # ####################################################

# class Sense(db.Model, SerializerMixin):
#     __tablename__ = "senses_table"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     distance = db.Column(db.Integer)
#     passive_score = db.Column(db.Integer)
#     monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
# # TODO: Add association on Monster


# # CHARACTER LANGUAGE ##################################
# # Example: Language(name="deep speech")
# # ####################################################

# class Language(db.Model):
#     __tablename__ = "languages_table"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
# # TODO: Add association on Monster


# # DAMAGE TYPE #########################################
# # Example: DamageResistance(name="cold")
# # 
# # DamageResistance, DamageImmunity, DamageVulnerability 
# # all require valid damage type
# # ####################################################

# # TODO: Clamp values to valid damage types
# # TODO: Add association on Monster

# class DamageResistance(db.Model):
#     __tablename__ = "damage_resistances_table"

#     id = db.Column(db.Integer, primary_key=True)
#     monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
#     damage_type = db.Column(db.String, nullable=False)

# class DamageImmunity(db.Model):
#     __tablename__ = "damage_immunities_table"

#     id = db.Column(db.Integer, primary_key=True)
#     monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
#     damage_type = db.Column(db.String, nullable=False)

# class DamageVulnerability(db.Model):
#     __tablename__ = "damage_vulnerabilities_table"

#     id = db.Column(db.Integer, primary_key=True)
#     monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
#     damage_type = db.Column(db.String, nullable=False)


# # CONDITION TYPE ######################################
# # Example: ConditionImmunity(name="charmed")
# # ####################################################

# # TODO: Clamp values to valid condition types
# # TODO: Add association on Monster

# class ConditionImmunity(db.Model):
#     __tablename__ = "condition_immunities_table"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))


# # CHARACTER ACTION ####################################
# # Example: Action(name="Club", description="Melee Weapon 
# # Attack: +2 to hit, reach 5ft., one target. Hit: 2 (1d4) 
# # bludgeoning damage.")
# # 
# # Actions belong to one monster
# # ####################################################

# class Action(db.Model):
#     __tablename__ = "actions_table"

#     id = db.Column(db.Integer, primary_key=True)
#     monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
#     legendary = db.Column(db.Boolean, default=False)
#     lair = db.Column(db.Boolean, default=False)
#     name = db.Column(db.String)
#     description = db.Column(db.String, nullable=False)
# # TODO: Add association on Monster


# # CHARACTER SPELL #####################################
# # Example: Spell()
# # 
# # MonsterSpell exists only as a join table
# # ####################################################

# class Spell(db.Model):
#     __tablename__ = "spells_table"

#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     description = db.Column(db.String)
#     level = db.Column(db.Integer, default=0)
#     casting_time = db.Column(db.String)
#     duration = db.Column(db.String)
#     range_area = db.Column(db.String)
    
#     verbal = db.Column(db.Boolean, default=False)
#     somatic = db.Column(db.Boolean, default=False)
#     material = db.Column(db.String)

#     school = db.Column(db.String)
#     attack_save = db.Column(db.String)
#     damage_type = db.Column(db.String)

# class MonsterSpell(db.Model):
#     __tablename__ = "monster_spells_table"

#     id = db.Column(db.Integer, primary_key=True)

#     spell_id = db.Column(db.Integer, db.ForeignKey("spells_table.id"))
#     spell = db.relationship("Spell", back_populates="monster_spells")

#     monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
#     monster = db.relationship("Monster", back_populates="monster_spells")
# # TODO: Add association on Monster
