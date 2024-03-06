from flask import Blueprint, request
from models import db, Spell, MonsterSpell
spell_routes_blueprint = Blueprint('spell_routes_blueprint', __name__)
from helpers import find_spell_by_id

# ------------------- SPELLS ROUTES ------------------- #

# GET SPELLS #########
# query params: page:int and page_count:int
# return spells:list[Spell:dict]
#######################
@spell_routes_blueprint.get('/spells')
def get_spells():
    PAGE = request.args.get('page') or 1
    PAGE_COUNT = request.args.get('page_count') or 10
    NAME_QUERY = request.args.get('name')
    SCHOOL_QUERY = request.args.get('school')
    OFFSET = (int(PAGE) - 1) * int(PAGE_COUNT)

    if NAME_QUERY or SCHOOL_QUERY:
        spells = Spell.query.where(
            Spell.name.like(f"%{NAME_QUERY}%") | 
            Spell.school.like(f"%{SCHOOL_QUERY}%")
        ).limit(PAGE_COUNT).offset(OFFSET).all()
    else:
        spells = Spell.query.limit(PAGE_COUNT).offset(OFFSET).all()

    return [ s.to_dict() for s in spells ], 200


# GET SPELL #########
# return Spell:dict
#######################
@spell_routes_blueprint.get('/spells/<int:id>')
def get_spell_by_id(id):
    s = find_spell_by_id(id)
    if s:
        return s.to_dict(), 200
    else:
        return { "error": "Not found" }, 404


# POST SPELL #########
# return Spell:dict
#######################
@spell_routes_blueprint.post('/spells')
def post_spell():
    data = request.json
    filtered_data = { k: v for k, v in data.items() 
                     if k in Spell.__table__.columns.keys() and k != 'id' } 

    try:
        NEW_S = Spell(**filtered_data)
        db.session.add(NEW_S)
        db.session.commit()

        return NEW_S.to_dict(), 201
    except ValueError as e:
        return { "error": f"{e}" }, 422

# PATCH SPELL #########
# return Spell:dict
#######################
@spell_routes_blueprint.patch('/spells/<int:id>')
def patch_spells(id):
    data = request.json
    filtered_data = { k: v for k, v in data.items() 
                     if k in Spell.__table__.columns.keys() and k != 'id' } 

    s = find_spell_by_id(id)

    if s:
        try:
            for k in filtered_data:
                setattr(s, k, filtered_data[k])

            db.session.commit()

            return s.to_dict(), 202

        except ValueError as e:
            return { "error": f"{e}" }, 422

    else:
        return { "error": "Not found" }, 404

# DELETE SPELL #########
# return None
#######################
@spell_routes_blueprint.delete('/spells/<int:id>')
def delete_spell(id):
    m = find_spell_by_id(id)

    if m:
        db.session.delete(m)
        db.session.commit()
        return {}, 204
    else:
        return { "error": "Not found" }, 404