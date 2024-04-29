from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from routes import monster_routes_blueprint, spell_routes_blueprint, create_nested_monster_routes_blueprint

from models import db, Monster, Skill, SavingThrow, SpecialAbility, Sense, Speed, Language, DamageResistance, DamageImmunity, DamageVulnerability, ConditionImmunity, Action, Spell, MonsterSpell

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

    CORS(app)




    # ------------------- ALL ROUTES ------------------- #

    @app.get('/')
    def index():
        return "Hello world"
    
    app.register_blueprint( monster_routes_blueprint )
    app.register_blueprint( spell_routes_blueprint )
    app.register_blueprint( create_nested_monster_routes_blueprint('skills', Skill) )
    app.register_blueprint( create_nested_monster_routes_blueprint('saving_throws', SavingThrow) )
    app.register_blueprint( create_nested_monster_routes_blueprint('special_abilities', SpecialAbility) )
    app.register_blueprint( create_nested_monster_routes_blueprint('senses', Sense) )
    app.register_blueprint( create_nested_monster_routes_blueprint('speeds', Speed) )
    app.register_blueprint( create_nested_monster_routes_blueprint('languages', Language) )
    app.register_blueprint( create_nested_monster_routes_blueprint('damage_resistances', DamageResistance) )
    app.register_blueprint( create_nested_monster_routes_blueprint('damage_immunities', DamageImmunity) )
    app.register_blueprint( create_nested_monster_routes_blueprint('damage_vulnerabilities', DamageVulnerability) )
    app.register_blueprint( create_nested_monster_routes_blueprint('condition_immunities', ConditionImmunity) )
    app.register_blueprint( create_nested_monster_routes_blueprint('actions', Action) )

    # SPELLS ROUTES #

    # MONSTER SPELLS ROUTES #



    return app