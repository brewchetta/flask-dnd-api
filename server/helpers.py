from models import db, Monster

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