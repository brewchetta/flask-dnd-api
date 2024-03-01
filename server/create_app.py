from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Monster, Skill, SavingThrow, SpecialAbility, Sense, Language, DamageResistance, DamageImmunity, DamageVulnerability, ConditionImmunity, Action, Spell, MonsterSpell

import config

# ###############################################
# mode: 'DEVELOPMENT', 'PRODUCTION', 'TESTING'
# return app:flask.app.Flask
# 
# create_app is a factory for app instance that
# uses proper db and testing params depending on
# environment
# ##############################################

def create_app(mode="DEVELOPMENT"):

    app = Flask(__name__)
    if mode == "PRODUCTION":
        app.config.from_object('config.ProductionConfig')
    elif mode == "DEVELOPMENT":
        app.config.from_object('config.DevelopmentConfig')
    elif mode == "TESTING":
        app.config.from_object('config.TestingConfig')
    else:
        raise TypeError(f"create_app requires a mode argument of 'PRODUCTION', 'DEVELOPMENT', or 'TESTING' but got {mode}")

    

    app.json.compact = False

    migrate = Migrate(app, db)

    db.init_app(app)

    # ----------- HELPER METHODS ----------- #
    
    # find_monster_by_id ##########
    # params: id:str
    # return Monster
    # ############################
    def find_monster_by_id(id):
        return Monster.query.where(Monster.id == id).first()
    
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



    # ----------- ROUTES ----------- #

    @app.get('/')
    def index():
        return "Hello world"
    
    # MONSTERS ROUTES #

    # GET MONSTERS #########
    # query params: page:int and page_count:int
    # return monsters:list[Monster:dict]
    #######################
    @app.get('/monsters')
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
    @app.get('/monsters/<int:id>')
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
    @app.post('/monsters')
    def post_monster():
        data = request.json
        filtered_data = { k: v for k, v in data.items() 
                         if k in dir(Monster) 
                         and '__' not in k 
                         and k not in ['skills', 'saving_throws', 'special_abilities', 'senses', 'languages', 'damage_resistances', 'damage_immunities', 'damage_vulnerabilities', 'condition_immunities', 'actions', 'spells', 'monster_spells'] } 
                        # add any additional validations for filtering data here including new associations

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
                replace_nested_monster_data(data['senses'], NEW_M, Language, ['name', 'distance'])
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

            db.session.commit()

            return NEW_M.to_dict(), 201
        except ValueError as e:
            return { "error": f"{e}" }, 422

    # PATCH MONSTER #########
    # return Monster:dict
    #######################
    @app.patch('/monsters/<int:id>')
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
                if data.get('saving_throws'):
                    replace_nested_monster_data(data['saving_throws'], m, SavingThrow, ['name', 'value'])
                if data.get('special_abilities'):
                    replace_nested_monster_data(data['special_abilities'], m, SpecialAbility, ['name', 'description'])
                if data.get('senses'):
                    replace_nested_monster_data(data['senses'], m, Language, ['name', 'distance'])
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

                db.session.commit()
                return m.to_dict(), 202
            except ValueError as e:
                return { "error": f"{e}" }, 422
        else:
            return { "error": "Not found" }, 404

    # DELETE MONSTER #########
    # return None
    #######################
    @app.delete('/monsters/<int:id>')
    def delete_monster(id):
        m = find_monster_by_id(id)

        if m:
            db.session.delete(m)
            db.session.commit()
            return {}, 204
        else:
            return { "error": "Not found" }, 404

    # SKILLS ROUTES #

    # GET MONSTERS SKILLS #########
    # return skills:list[Skill:dict]
    #######################
    @app.get('/monsters/<int:id>/skills')
    def get_monster_skills(id):
        m = find_monster_by_id(id)
        if m:
            return [ s.to_dict(rules=("-monster", "-monster_id")) for s in m.skills ]
        else:
            return { "error": "Not found" }, 404

    # PATCH MONSTERS SKILLS #########
    # return Skill:dict
    #######################
    @app.patch('/monsters/<int:monster_id>/skills/<int:id>')
    def patch_monster_skill(monster_id, id):
        data = request.json
        filtered_data = { k: v for k, v in data.items() if k in ['name', 'value'] }
        m = find_monster_by_id(monster_id)
        s = Skill.query.where(Skill.id == id).first()
        if m and s:
            try:
                for key in filtered_data:
                    setattr(s, key, data[key])
                db.session.commit()
                return s.to_dict(), 202
            except ValueError as e:
                return { 'error': f"{e}" }, 422
        else:
            return { "error": "Not found" }, 404

    # DELETE MONSTERS SKILLS #########
    # return None
    #######################
    @app.delete('/monsters/<int:monster_id>/skills/<int:id>')
    def delete_monster_skill(monster_id, id):
        m = find_monster_by_id(monster_id)
        s = Skill.query.where(Skill.id == id).first()
        if m and s:
            db.session.delete(s)
            db.session.commit()
            return {}, 204
        else:
            return { "error": "Not found" }, 404
        
    # SAVING THROWS ROUTES #

    # GET MONSTERS SAVING THROWS #########
    # return saving_throws:list[SavingThrow:dict]
    #######################
    @app.get('/monsters/<int:id>/saving-throws')
    def get_monster_saving_throws(id):
        m = find_monster_by_id(id)
        if m:
            return [ s.to_dict(rules=("-monster", "-monster_id")) for s in m.saving_throws ]
        else:
            return { "error": "Not found" }, 404

    # PATCH MONSTERS SAVING THROWS #########
    # return SavingThrow:dict
    #######################
    @app.patch('/monsters/<int:monster_id>/saving-throws/<int:id>')
    def patch_monster_saving_throw(monster_id, id):
        data = request.json
        filtered_data = { k: v for k, v in data.items() if k in ['name', 'value'] }
        m = find_monster_by_id(monster_id)
        s = SavingThrow.query.where(SavingThrow.id == id).first()
        if m and s:
            try:
                for key in filtered_data:
                    setattr(s, key, data[key])
                db.session.commit()
                return s.to_dict(), 202
            except ValueError as e:
                return { 'error': f"{e}" }, 422
        else:
            return { "error": "Not found" }, 404

    # DELETE MONSTERS SAVING THROWS #########
    # return None
    #######################
    @app.delete('/monsters/<int:monster_id>/saving-throws/<int:id>')
    def delete_monster_saving_throw(monster_id, id):
        m = find_monster_by_id(monster_id)
        s = SavingThrow.query.where(SavingThrow.id == id).first()
        if m and s:
            db.session.delete(s)
            db.session.commit()
            return {}, 204
        else:
            return { "error": "Not found" }, 404

    # SENSES ROUTES #

    # LANGUAGES ROUTES #

    # DAMAGE RESISTANCES ROUTES #

    # DAMAGE IMMUNITIES ROUTES #

    # DAMAGE VULNERABILITIES ROUTES #

    # CONDITION IMMUNITIES ROUTES #

    # ACTIONS ROUTES #

    # SPELLS ROUTES #

    # MONSTER SPELLS ROUTES #



    return app