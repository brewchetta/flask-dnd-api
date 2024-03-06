from flask import Blueprint, request
from models import db, Monster, Skill, SavingThrow, SpecialAbility, Sense, Language, DamageResistance, DamageImmunity, DamageVulnerability, ConditionImmunity, Action, Spell, MonsterSpell
monster_routes_blueprint = Blueprint('monster_routes_blueprint', __name__)
from helpers import replace_nested_monster_data, find_monster_by_id, replace_associated_monster_spells

# ------------------- MONSTERS ROUTES ------------------- #

# GET MONSTERS #########
# query params: page:int and page_count:int
# return monsters:list[Monster:dict]
#######################
@monster_routes_blueprint.get('/monsters')
def get_monsters():
    PAGE = request.args.get('page') or 1
    PAGE_COUNT = request.args.get('page_count') or 10
    NAME_QUERY = request.args.get('name')
    CATEGORY_QUERY = request.args.get('category')
    SUBCATEGORY_QUERY = request.args.get('sub_category')
    SIZE_QUERY = request.args.get('size')
    OFFSET = (int(PAGE) - 1) * int(PAGE_COUNT)

    if NAME_QUERY or CATEGORY_QUERY or SUBCATEGORY_QUERY or SIZE_QUERY:
        monsters = Monster.query.where(
            Monster.name.like(f"%{NAME_QUERY}%") | 
            Monster.category.like(f"%{CATEGORY_QUERY}%") | 
            Monster.sub_category.like(f"%{SUBCATEGORY_QUERY}%") | 
            Monster.size.like(f"%{SIZE_QUERY}%")
        ).limit(PAGE_COUNT).offset(OFFSET).all()
    else:
        monsters = Monster.query.limit(PAGE_COUNT).offset(OFFSET).all()

    return [ m.to_dict() for m in monsters ], 200


# GET MONSTER #########
# return Monster:dict
#######################
@monster_routes_blueprint.get('/monsters/<int:id>')
def get_monster_by_id(id):
    m = find_monster_by_id(id)
    if m:
        return m.to_dict(), 200
    else:
        return { "error": "Not found" }, 404


# POST MONSTER #########
# return Monster:dict
#######################
# TODO: able to accept list of skills to associate
@monster_routes_blueprint.post('/monsters')
def post_monster():
    data = request.json
    filtered_data = { k: v for k, v in data.items() 
                     if k in Monster.__table__.columns.keys() and k != 'id' } 

    try:
        NEW_M = Monster(**filtered_data)
        db.session.add(NEW_M)

        if data.get('skills'):
            replace_nested_monster_data(data['skills'], NEW_M, Skill, ['name', 'value'])
        if data.get('saving_throws'):
            replace_nested_monster_data(data['saving_throws'], NEW_M, SavingThrow, ['name', 'value'])
        if data.get('saving_throws'):
            replace_nested_monster_data(data['saving_throws'], NEW_M, SavingThrow, ['name', 'value'])
        if data.get('special_abilities'):
            replace_nested_monster_data(data['special_abilities'], NEW_M, SpecialAbility, ['name', 'description'])
        if data.get('senses'):
            replace_nested_monster_data(data['senses'], NEW_M, Sense, ['name', 'distance'])
        if data.get('languages'):
            replace_nested_monster_data(data['languages'], NEW_M, Language, ['name'])
        if data.get('damage_resistances'):
            replace_nested_monster_data(data['damage_resistances'], NEW_M, DamageResistance, ['damage_type'])
        if data.get('damage_immunities'):
            replace_nested_monster_data(data['damage_immunities'], NEW_M, DamageImmunity, ['damage_type'])
        if data.get('damage_vulnerabilities'):
            replace_nested_monster_data(data['damage_vulnerabilities'], NEW_M, DamageVulnerability, ['damage_type'])
        if data.get('condition_immunities'):
            replace_nested_monster_data(data['condition_immunities'], NEW_M, ConditionImmunity, ['condition_type'])
        if data.get('actions'):
            replace_nested_monster_data(data['actions'], NEW_M, Action, ['legendary_action', 'lair_action', 'name', 'description'])
        
        if data.get('spells'):
            replace_associated_monster_spells(data['spells'], NEW_M)
            

        db.session.commit()

        return NEW_M.to_dict(), 201
    except ValueError as e:
        return { "error": f"{e}" }, 422

# PATCH MONSTER #########
# return Monster:dict
#######################
@monster_routes_blueprint.patch('/monsters/<int:id>')
def patch_monster(id):
    data = request.json
    filtered_data = { k: v for k, v in data.items() 
                        if k in dir(Monster) 
                        and '__' not in k 
                        and k not in ['skills', 'saving_throws', 'special_abilities', 'senses', 'languages', 'damage_resistances', 'damage_immunities', 'damage_vulnerabilities', 'condition_immunities', 'actions', 'spells', 'monster_spells'] } 
                    # add any additional validations for filtering data here including new associations

    m = find_monster_by_id(id)

    if m:
        try:
            for k in filtered_data:
                setattr(m, k, filtered_data[k])

            if data.get('skills'):
                replace_nested_monster_data(data['skills'], m, Skill, ['name', 'value'])
            if data.get('saving_throws'):
                replace_nested_monster_data(data['saving_throws'], m, SavingThrow, ['name', 'value'])
            if data.get('special_abilities'):
                replace_nested_monster_data(data['special_abilities'], m, SpecialAbility, ['name', 'description'])
            if data.get('senses'):
                replace_nested_monster_data(data['senses'], m, Sense, ['name', 'distance'])
            if data.get('languages'):
                replace_nested_monster_data(data['languages'], m, Language, ['name'])
            if data.get('damage_resistances'):
                replace_nested_monster_data(data['damage_resistances'], m, DamageResistance, ['damage_type'])
            if data.get('damage_immunities'):
                replace_nested_monster_data(data['damage_immunities'], m, DamageImmunity, ['damage_type'])
            if data.get('damage_vulnerabilities'):
                replace_nested_monster_data(data['damage_vulnerabilities'], m, DamageVulnerability, ['damage_type'])
            if data.get('condition_immunities'):
                replace_nested_monster_data(data['condition_immunities'], m, ConditionImmunity, ['condition_type'])
            if data.get('actions'):
                replace_nested_monster_data(data['actions'], m, Action, ['legendary_action', 'lair_action', 'name', 'description'])

            if data.get('spells'):
                replace_associated_monster_spells(data['spells'], m)

            db.session.commit()
            return m.to_dict(), 202
        except ValueError as e:
            return { "error": f"{e}" }, 422
    else:
        return { "error": "Not found" }, 404

# DELETE MONSTER #########
# return None
#######################
@monster_routes_blueprint.delete('/monsters/<int:id>')
def delete_monster(id):
    m = find_monster_by_id(id)

    if m:
        db.session.delete(m)
        db.session.commit()
        return {}, 204
    else:
        return { "error": "Not found" }, 404
    

# ------------------- MONSTER SPELLS ROUTES ------------------- #

# POST MONSTER SPELL #########
# return MonsterSpell:dict
#######################
@monster_routes_blueprint.post('/monster/<int:id>/monster-spells')
def create_monster_spell(id):
    data = request.json
    spell_name = data.get('spell_name')
    spell_id = data.get('spell_id')

    m = find_monster_by_id(id)
    s = Spell.query.where(
        Spell.name == spell_name |
        Spell.id == spell_id
    ).first()

    if m and s:
        try:
            ms = MonsterSpell(monster=m, spell=s)
            db.session.add(ms)
            db.session.commit()
            return ms.to_dict(), 201
        except ValueError as e:
            return { "error": f"{e}" }, 422
    else:
        return { "error": "Monster or spell not found" }, 404

# DELETE MONSTER SPELL #########
# return None
#######################
@monster_routes_blueprint.post('/monster/<int:monster_id>/monster-spells/<int:id>')
def create_monster_spell(monster_id, id):
    m = find_monster_by_id(monster_id)
    ms = MonsterSpell.query.where(MonsterSpell.id == id).first()

    if m and ms:
        db.session.delete(ms)
        db.session.commit()
        return {}, 204
    else:
        return { "error": "Not found" }, 404