from flask import Blueprint, request
from models import db, Monster
from helpers import replace_nested_monster_data, find_monster_by_id

# create_nested_monster_routes_blueprint ####################
# name:str = pluralized name of resource being added
# model:class = model being used by this blueprint
# 
# example: create_nested_monster_routes_blueprint
# ################################################
def create_nested_monster_routes_blueprint(name, model):
    nested_blueprint = Blueprint(f'{name}_routes_blueprint', __name__)
    
    # GET MONSTERS RESOURCES #########
    # return models:list[model:dict]
    #################################
    @nested_blueprint.get(f"/monsters/<int:id>/{name.replace('_', '-')}")
    def get_monster_languages(id):
        m = find_monster_by_id(id)
        if m:
            return [ item.to_dict(rules=("-monster", "-monster_id")) for item in model.query.where(model.monster_id == id).all() ]
        else:
            return { "error": "Not found" }, 404

    # PATCH MONSTERS RESOURCE #########
    # return model:dict
    ##################################
    @nested_blueprint.patch(f"/monsters/<int:monster_id>/{name.replace('_', '-')}/<int:id>")
    def patch_monster_language(monster_id, id):
        data = request.json
        filtered_data = { k: v for k, v in data.items() if k in model.__table__.columns.keys() and k != 'id' }
        m = find_monster_by_id(monster_id)
        item = model.query.where(model.id == id).first()
        if m and item:
            try:
                for key in filtered_data:
                    setattr(item, key, data[key])
                db.session.commit()
                return item.to_dict(), 202
            except ValueError as e:
                return { 'error': f"{e}" }, 422
        else:
            return { "error": "Not found" }, 404

    # DELETE MONSTERS RESOURCE #########
    # return None
    ###################################
    @nested_blueprint.delete(f"/monsters/<int:monster_id>/{name.replace('_', '-')}/<int:id>")
    def delete_monster_language(monster_id, id):
        m = find_monster_by_id(monster_id)
        item = model.query.where(model.id == id).first()
        if m and item:
            db.session.delete(item)
            db.session.commit()
            return {}, 204
        else:
            return { "error": "Not found" }, 404
        
    return nested_blueprint