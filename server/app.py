#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db, Monster

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.get('/')
def index():
    return "Hello world"

# GET MONSTERS #########
# query params: page:int and per_page:int
# return monsters:list[Monster:dict]
#######################
@app.get('/monsters')
def get_monsters():
    PAGE = request.args.get('page') or 1
    PER_PAGE = request.args.get('per_page') or 10
    OFFSET = (PAGE - 1) * PER_PAGE

    monsters = Monster.query.limit(PER_PAGE).offset(OFFSET).all()
    return [ m.to_dict() for m in monsters ]


# POST MONSTER #########
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


if __name__ == '__main__':
    app.run(port=5555, debug=True)