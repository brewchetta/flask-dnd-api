import os
import re
import json
from create_app import create_app
from models import db, Monster, Skill, SavingThrow, SpecialAbility, Sense, Speed, Language, DamageResistance, DamageImmunity, DamageVulnerability, ConditionImmunity, Action, Spell, MonsterSpell
from helpers import replace_nested_monster_data, replace_associated_monster_spells

DEBUG = True

def debug_print(*args):
    if DEBUG:
        print(*args)

app = create_app()

with app.app_context():

    print("Removing old data")

    MonsterSpell.query.delete()
    Spell.query.delete()
    Skill.query.delete()
    SavingThrow.query.delete()
    SpecialAbility.query.delete()
    Sense.query.delete()
    Speed.query.delete()
    Language.query.delete()
    DamageResistance.query.delete()
    DamageImmunity.query.delete()
    DamageVulnerability.query.delete()
    ConditionImmunity.query.delete()
    Action.query.delete()
    Monster.query.delete()

    print("Currently registered spells:")
    print([spell.name for spell in Spell.query.all()])

    path = "./beyond_json_data/spells"
    dir_list = os.listdir(path)
    print(f"\nReading all files in {path}...")

    for file_name in dir_list:
        print(f'\nOpening {file_name}...')
        with open(f"{path}/{file_name}") as json_file:
            spell_json = json.load(json_file)
            print(f" Building {spell_json.get('name') or 'null_spell_name'}")

            filtered_data = { k: v for k, v in spell_json.items() 
                     if k in Spell.__table__.columns.keys() and k != 'id' }
            
            Spell.query.where(Spell.name == filtered_data.get('name')).delete()
            NEW_S = Spell(**filtered_data)
            db.session.add(NEW_S)

    debug_print("\nCurrently registered spells:")
    debug_print([s.name for s in Spell.query.all()])





    print("Currently registered monsters:")
    print([m.name for m in Monster.query.all()])

    path = "./beyond_json_data/monsters"
    dir_list = os.listdir(path)
    print(f"\nReading all files in {path}...")

    for file_name in dir_list:
        print(f"\nOpening {file_name}...")
        with open(f"{path}/{file_name}") as json_file:
            monster_json = json.load(json_file)
            print(f" Building {monster_json.get('name') or 'null_monster_name'}")

            monster_json['category'] = monster_json.get('type').replace(",", "")
            monster_json['sub_category'] = monster_json.get('subtype')
            monster_json['hit_dice_count'] = int(monster_json.get('hit_dice').strip().split('d')[0])
            monster_json['hit_dice_size'] = int(monster_json.get('hit_dice').strip().split('d')[1])
            if monster_json['hit_dice_size'] == 1:
                monster_json['hit_dice_size'] == 10
            if monster_json['challenge_rating'] == "1/4":
                monster_json['challenge_rating'] = 0.25
            if monster_json['challenge_rating'] == "1/2":
                monster_json['challenge_rating'] = 0.5
            if monster_json.get('spell_dc'):
                monster_json['spell_save_dc'] = monster_json['spell_dc']

            filtered_data = { k: v for k, v in monster_json.items() 
                     if k in Monster.__table__.columns.keys() and k != 'id' } 

            Monster.query.where(Monster.name == filtered_data.get('name')).delete()
            NEW_M = Monster(**filtered_data)
            db.session.add(NEW_M)


            # SKILLS / SAVES (PROFICIENCIES)

            if monster_json.get('proficiencies'):
                proficiencies = monster_json['proficiencies'].split('|')
                for prof in proficiencies:
                    if "Saving Throw:" in prof:
                        prof_kv = prof.replace('Saving Throw:', '').strip().split()
                        new_st = SavingThrow(name=prof_kv[0], value=int(prof_kv[1]), monster=NEW_M)
                        db.session.add(new_st)
                    if "Skill:" in prof:
                        prof_kv = prof.replace('Skill:', '').replace('Animal Handling', 'Animal_Handling').strip().split()
                        new_sk = Skill(name=prof_kv[0].replace("_", " "), value=int(prof_kv[1]), monster=NEW_M)
                        db.session.add(new_sk)

            for s in NEW_M.saving_throws:
                debug_print(f"  saving throw - {s.name}: {s.value}")
            for s in NEW_M.skills:
                debug_print(f"  skill - {s.name}: {s.value}")


            # LANGUAGES
                
            if monster_json.get('languages'):
                languages = monster_json['languages'].split(', ')
                for language in languages:
                    if language != '--':
                        l = Language(name=language, monster=NEW_M)
                        db.session.add(l)

            for l in NEW_M.languages:
                debug_print(f"  language - {l.name}")


            # SENSES
                
            if monster_json.get('senses'):
                senses = monster_json['senses'].split('|')
                for sense in senses:
                    if "passive perception" in sense.lower():
                        NEW_M.passive_perception = int(sense.strip().split(" ")[-1])
                    else:
                        sense_attrs = sense.lower().strip().replace("ft.","").split(" ")
                        print(sense_attrs)
                        s = Sense(name=sense_attrs[0], distance=int(sense_attrs[1]), monster=NEW_M)
                    db.session.add(s)

            for s in NEW_M.senses:
                debug_print(f"  sense - {s.name}: {s.distance}")

            debug_print(f"  passive perception - {NEW_M.passive_perception}")


            # SPECIAL ABILITIES

            if monster_json.get('special_abilities'):
                for sa in monster_json['special_abilities']:
                    sa['description'] = sa['desc']
                    if 'spellcasting ability is' in sa['description'].lower():
                        match = re.search("spellcasting ability is (\w+)", sa['description'])
                        NEW_M.spellcasting_ability = match.group(1)
                    if 'as the spellcasting ability' in sa['description'].lower():
                        match = re.search("(\w+) as the spellcasting ability", sa['description'])
                        NEW_M.spellcasting_ability = match.group(1)

                replace_nested_monster_data(monster_json['special_abilities'], NEW_M, SpecialAbility, ['name', 'description'])

            for s in NEW_M.special_abilities:
                debug_print(f"  special ability - {s.name}: {s.description}")

            # ACTIONS

            if monster_json.get('actions'):
                for act in monster_json['actions']:
                    act['description'] = act['desc']
                    if 'spellcasting ability is' in act['description'].lower():
                        match = re.search("spellcasting ability is (\w+)", act['description'])
                        NEW_M.spellcasting_ability = match.group(1)
                    if 'as the spellcasting ability' in act['description'].lower():
                        match = re.search("(\w+) as the spellcasting ability", act['description'])
                        NEW_M.spellcasting_ability = match.group(1)
                replace_nested_monster_data(monster_json['actions'], NEW_M, Action, ['name', 'description'])

            for s in NEW_M.actions:
                debug_print(f"  action - {s.name}: {s.description}")

            # DAMAGE RESISTANCES

            if monster_json.get('damage_resistances'):
                monster_json['damage_resistances'] = [ { 'damage_type': dr } for dr in monster_json['damage_resistances'] ]
                replace_nested_monster_data(monster_json['damage_resistances'], NEW_M, DamageResistance, ['damage_type'])

            # DAMAGE IMMUNITIES

            if monster_json.get('damage_immunities'):
                monster_json['damage_immunities'] = [ { 'damage_type': di } for di in monster_json['damage_immunities'] ]
                replace_nested_monster_data(monster_json['damage_immunities'], NEW_M, DamageImmunity, ['damage_type'])

            # DAMAGE VULNERABILITIES

            if monster_json.get('damage_vulnerabilities'):
                monster_json['damage_vulnerabilities'] = [ { 'damage_type': dv } for dv in monster_json['damage_vulnerabilities'] ]
                replace_nested_monster_data(monster_json['damage_vulnerabilities'], NEW_M, DamageVulnerability, ['damage_type'])

            # CONDITION IMMUNITIES

            if monster_json.get('condition_immunities'):
                monster_json['condition_immunities'] = [ { 'condition_type': ci } for ci in monster_json['condition_immunities'] ]
                replace_nested_monster_data(monster_json['condition_immunities'], NEW_M, ConditionImmunity, ['condition_type'])

            for dv in NEW_M.damage_vulnerabilities:
                debug_print(f"  damage_vulnerability - {dv.damage_type}")

            for dr in NEW_M.damage_resistances:
                debug_print(f"  damage_resistance - {dr.damage_type}")

            for di in NEW_M.damage_immunities:
                debug_print(f"  damage_immunity - {di.damage_type}")

            for ci in NEW_M.condition_immunities:
                debug_print(f"  condition_immunity - {ci.condition_type}")

            # SPEEDS

            if monster_json.get('speed'):
                for k in monster_json['speed'].keys():
                    sp = Speed(monster=NEW_M, name=k, distance=monster_json['speed'][k])
                    db.session.add(sp)

            for sp in NEW_M.speeds:
                debug_print(f"  speed - {sp.name}: {sp.distance}")

            # SPELL SLOTS

            if monster_json['spell_slots']:
                for k in monster_json['spell_slots']:
                    if k == "1":
                        NEW_M.spell_slots_first_level = monster_json['spell_slots'][k]
                    if k == "2":
                        NEW_M.spell_slots_second_level = monster_json['spell_slots'][k]
                    if k == "3":
                        NEW_M.spell_slots_third_level = monster_json['spell_slots'][k]
                    if k == "4":
                        NEW_M.spell_slots_fourth_level = monster_json['spell_slots'][k]
                    if k == "5":
                        NEW_M.spell_slots_fifth_level = monster_json['spell_slots'][k]
                    if k == "6":
                        NEW_M.spell_slots_sixth_level = monster_json['spell_slots'][k]
                    if k == "7":
                        NEW_M.spell_slots_seventh_level = monster_json['spell_slots'][k]
                    if k == "8":
                        NEW_M.spell_slots_eighth_level = monster_json['spell_slots'][k]
                    if k == "9":
                        NEW_M.spell_slots_ninth_level = monster_json['spell_slots'][k]

            for k in NEW_M.__table__.columns.keys():
                debug_print(f"  {k} - {getattr(NEW_M, k)}")


            # if monster_json.get('spells'):
            #     replace_associated_monster_spells(monster_json['spells'], NEW_M)

            # except Exception as e:
            #     print(f"ERROR: {e}")
                
            # import ipdb; ipdb.set_trace()
    
    debug_print("\nCurrently registered monsters:")
    debug_print([m.name for m in Monster.query.all()])

    # TODO: Build json converter for spells
    # TODO: Monster can add spells
    # TODO: Scraper gets flat proficiency bonus
    # TODO: Scraper properly gets legendary actions and lair actions
    # TODO: Scraper gets at will spells that aren't cantrips
    # TODO: Scraper gets inherent spells (see annis hag)