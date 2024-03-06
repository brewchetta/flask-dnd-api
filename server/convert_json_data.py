import os
import json
from create_app import create_app
from models import db, Monster, Skill, SavingThrow, SpecialAbility, Sense, Speed, Language, DamageResistance, DamageImmunity, DamageVulnerability, ConditionImmunity, Action
from helpers import replace_nested_monster_data, replace_associated_monster_spells

app = create_app()

with app.app_context():

    print("Currently registered monsters:")
    print([m.name for m in Monster.query.all()])

    path = "./beyond_json_data"
    dir_list = os.listdir(path)
    print(f"\nReading all files in {path}...")

    for file_name in dir_list:
        print(f"\nOpening {file_name}...")
        with open(f"{path}/{file_name}") as json_file:
            monster_json = json.load(json_file)
            print(f" Building {monster_json.get('name') or 'null_monster_name'}")

            filtered_data = { k: v for k, v in monster_json.items() 
                     if k in Monster.__table__.columns.keys() and k != 'id' } 

            # try:
            Monster.query.where(Monster.name == filtered_data.get('name')).delete()
            NEW_M = Monster(**filtered_data)
            db.session.add(NEW_M)

            if monster_json.get('proficiencies'):
                replace_nested_monster_data(monster_json['skills'], NEW_M, Skill, ['name', 'value'])
            if monster_json.get('saving_throws'):
                replace_nested_monster_data(monster_json['saving_throws'], NEW_M, SavingThrow, ['name', 'value'])
            if monster_json.get('special_abilities'):
                replace_nested_monster_data(monster_json['special_abilities'], NEW_M, SpecialAbility, ['name', 'description'])
            if monster_json.get('senses'):
                replace_nested_monster_data(monster_json['senses'], NEW_M, Sense, ['name', 'distance'])
            if monster_json.get('speeds'):
                replace_nested_monster_data(monster_json['speeds'], NEW_M, Speed, ['name', 'distance'])
            if monster_json.get('languages'):
                replace_nested_monster_data(monster_json['languages'], NEW_M, Language, ['name'])
            if monster_json.get('damage_resistances'):
                replace_nested_monster_data(monster_json['damage_resistances'], NEW_M, DamageResistance, ['damage_type'])
            if monster_json.get('damage_immunities'):
                replace_nested_monster_data(monster_json['damage_immunities'], NEW_M, DamageImmunity, ['damage_type'])
            if monster_json.get('damage_vulnerabilities'):
                replace_nested_monster_data(monster_json['damage_vulnerabilities'], NEW_M, DamageVulnerability, ['damage_type'])
            if monster_json.get('condition_immunities'):
                replace_nested_monster_data(monster_json['condition_immunities'], NEW_M, ConditionImmunity, ['condition_type'])
            if monster_json.get('actions'):
                replace_nested_monster_data(monster_json['actions'], NEW_M, Action, ['legendary_action', 'lair_action', 'name', 'description'])
            
            if monster_json.get('spells'):
                replace_associated_monster_spells(monster_json['spells'], NEW_M)

            # except Exception as e:
            #     print(f"ERROR: {e}")
    
    print("Currently registered monsters:")
    print([m.name for m in Monster.query.all()])