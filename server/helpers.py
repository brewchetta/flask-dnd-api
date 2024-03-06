from models import db, Monster, Spell, MonsterSpell

# ----------- HELPER METHODS ----------- #


# find_monster_by_id ##########
# params: id:str
# return Monster
# ############################
def find_monster_by_id(id):
    return Monster.query.where(Monster.id == id).first()


# find_spell_by_id ##########
# params: id:str
# return Spell
# ############################
def find_spell_by_id(id):
    return Spell.query.where(Spell.id == id).first()


# find_spell_by_name ##########
# params: id:str
# return Spell
# ############################
def find_spell_by_name(name):
    return Spell.query.where(Spell.name == name).first()


# replace_nested_monster_data #################
# params: data:list[dict], parent:Monster, 
# child_class:class, valid_attributes:list[str]
# 
# return list[child_class_instance]
# ###########################################
def replace_nested_monster_data(data, parent, child_class, valid_attributes):
    child_class.query.where(child_class.monster_id == parent.id).delete()
    new_items = []
    for item_dict in data:
        filtered_item_dict = { k: v for k, v in item_dict.items() if k in valid_attributes }
        new_item = child_class(**filtered_item_dict)
        new_item.monster = parent
        db.session.add(new_item)
        new_items.append(new_item)
    return new_item

# replace_associated_monster_spells #################
# params: spell_names:list[str], parent:Monster, 
# 
# return list[MonsterSpell:instance]
# ###########################################
def replace_associated_monster_spells(spell_names, parent):
    MonsterSpell.query.where(MonsterSpell.monster == parent).delete()
    new_joins = []
    for s_name in spell_names:
        spell = find_spell_by_name(s_name)
        if spell:
            try:
                ms = MonsterSpell(monster=parent, spell=spell)
                db.session.add(ms)
                db.session.commit()
                new_joins.append(ms)
            except Exception as e:
                print(f"An exception has occurred: {e}")
    return new_joins