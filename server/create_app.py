from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Monster, Skill, SavingThrow

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
                         and k not in ['skills', 'saving_throws', 'special_abilities', 'senses', 'languages', 'damage_resistances', 'damage_immunities', 'damage_vulnerabilities', 'condition_immunities', 'actions', 'spells', 'monster_spells']
                         and 'saving_throws' not in k } 
                        # add any additional validations for filtering data here including new associations

        try:
            NEW_M = Monster(**filtered_data)
            db.session.add(NEW_M)

            # conditionally add skills
            if data.get('skills'):
                for skill_data in data['skills']:
                    filtered_skill_data = { k: v for k, v in skill_data.items() if k in dir(Skill) and '__' not in k }
                    NEW_SKILL = Skill(**filtered_skill_data)
                    NEW_SKILL.monster = NEW_M
                    db.session.add(NEW_SKILL)

            # conditionally add saving throws
            if data.get('saving_throws'):
                for skill_data in data['saving_throws']:
                    filtered_skill_data = { k: v for k, v in skill_data.items() if k in dir(SavingThrow) and '__' not in k }
                    NEW_SAVE = SavingThrow(**filtered_skill_data)
                    NEW_SAVE.monster = NEW_M
                    db.session.add(NEW_SAVE)

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
        filtered_data = { k: v for k, v in data.items() if k in dir(Monster) and '__' not in k }
        m = find_monster_by_id(id)

        if m:
            try:
                for k in filtered_data:
                    setattr(m, k, filtered_data[k])
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


    return app