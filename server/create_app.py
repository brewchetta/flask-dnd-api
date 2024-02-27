from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Monster

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

    @app.get('/')
    def index():
        return "Hello world"

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
        monster = Monster.query.where(Monster.id == id).first()
        return monster.to_dict(), 200


    # POST MONSTER #########
    # return Monster:dict
    #######################
    @app.post('/monsters')
    def post_monster():
        data = request.json
        filtered_data = { k: v for k, v in data.items() if k in dir(Monster) and '__' not in k }
        try:
            NEW_M = Monster(**filtered_data)
            db.session.add(NEW_M)
            db.session.commit()
            return NEW_M.to_dict(), 201
        except ValueError as e:
            return { "error": f"An error occurred: {e}" }, 406

    return app