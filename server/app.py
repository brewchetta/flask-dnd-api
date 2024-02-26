#!/usr/bin/env python3

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import db # import your models here!

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

    monsters = Monsters.query.limit(PER_PAGE).offset(OFFSET).all()
    return [ m.to_dict() for m in monsters ]


if __name__ == '__main__':
    app.run(port=5555, debug=True)