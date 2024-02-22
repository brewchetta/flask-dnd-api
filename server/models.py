from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# MONSTER #############################################
# ####################################################

class Monster(db.Model):
    __tablename__ = "monsters_table"

    id = db.Column(db.Integer, primary_key=True)

    monster_category_id = db.Column(db.Integer, db.ForeignKey("monster_categories_table.id"))

    name = db.Column(db.String, nullable=False)
    size = db.Column(db.String, default="medium")

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

    spellcasting_level = db.Column(db.Integer)
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


# CHARACTER CATEGORY #################################
# Examples: humanoid, construct, infernal, etc.
# ####################################################

class CharacterCategory(db.Model):
    __tablename__ = "monster_categories_table"

    id = db.Column(db.Integer, primary_key=True)

# CHARACTER SKILL #####################################
# a +2 to History would have Skill(name="history")
# and SkillValue(value="2") along with foreign keys
# ####################################################
    

class Skill(db.Model):
    __tablename__ = "skills_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class SkillValue(db.Model):
    __tablename__ = "skill_values_table"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer, default=0)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills_table.id"))
    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))

# CHARACTER SAVING THROW ##############################
# ####################################################

class SavingThrow(db.Model):
    __tablename__ = "saving_throws_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class SavingThrowValue(db.Model):
    __tablename__ = "saving_throw_values_table"

    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.String)
    saving_throw_id = db.Column(db.Integer, db.ForeignKey("saving_throws_table.id"))
    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))

# CHARACTER SPECIAL ABILITY ###########################
# Example: SpecialAbility(name="Amphibious", 
# description="The monster can breath water and air")
# 
# MonsterSpecialAbility exists only as join table
# ####################################################

class SpecialAbility(db.Model):
    __tablename__ = "special_abilities_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

class MonsterSpecialAbility(db.Model):
    __tablename__ = "monster_special_abilities_table"

    id = db.Column(db.Integer, primary_key=True)
    special_ability_id = db.Column(db.Integer, db.ForeignKey("special_abilities_table.id"))
    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))

# CHARACTER SENSE #####################################
# Example: Sense(name="darkvision")
# Example MonsterSense(distance=120)
# 
# Example: Sense(name="passive perception")
# Example MonsterSense(passive_score=12)
# ####################################################

class Sense(db.Model):
    __tablename__ = "senses_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class MonsterSense(db.Model):
    __tablename__ = "monster_senses_table"

    id = db.Column(db.Integer, primary_key=True)
    sense_id = db.Column(db.Integer, db.ForeignKey("senses_table.id"))
    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
    distance = db.Column(db.Integer)
    passive_score = db.Column(db.Integer)

# CHARACTER LANGUAGE ##################################
# Example: Language(name="deep speech")
# 
# MonsterLanguage exists as join table
# ####################################################

class Language(db.Model):
    __tablename__ = "languages_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

class MonsterLanguage(db.Model):
    __tablename__ = "monster_languages_table"

    id = db.Column(db.Integer, primary_key=True)
    language_id = db.Column(db.Integer, db.ForeignKey("languages_table.id"))
    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))

# CHARACTER ACTION ####################################
# Example: Action(name="Club", description="Melee Weapon Attack: +2 to hit, reach 5ft., one target. Hit: 2 (1d4) bludgeoning damage.")
# 
# Actions belong to one monster
# ####################################################

class Action(db.Model):
    __tablename__ = "actions_table"

    id = db.Column(db.Integer, primary_key=True)
    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))
    legendary = db.Column(db.Boolean, default=False)
    lair = db.Column(db.Boolean, default=False)
    name = db.Column(db.String)
    description = db.Column(db.String, nullable=False)

# CHARACTER SPELL #####################################
# Example: Spell()
# 
# MonsterSpell exists only as a join table
# ####################################################

class Spell(db.Model):
    __tablename__ = "spells_table"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String)
    level = db.Column(db.Integer, default=0)
    casting_time = db.Column(db.String)
    duration = db.Column(db.String)
    range_area = db.Column(db.String)
    
    verbal = db.Column(db.Boolean, default=False)
    somatic = db.Column(db.Boolean, default=False)
    material = db.Column(db.String)

    school = db.Column(db.String)
    attack_save = db.Column(db.String)
    damage_type = db.Column(db.String)

class MonsterSpell(db.Model):
    __tablename__ = "monster_spells_table"

    id = db.Column(db.Integer, primary_key=True)
    spell_id = db.Column(db.Integer, db.ForeignKey("spells_table.id"))
    monster_id = db.Column(db.Integer, db.ForeignKey("monsters_table.id"))