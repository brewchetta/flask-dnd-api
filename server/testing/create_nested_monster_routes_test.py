import pytest
from create_app import create_app
from models import db, Monster
from testing.test_monsters import MONSTER_ONE, MONSTER_TWO

app = create_app('TESTING')

# create_nested_monster_routes_test #################################################
# model_name:str = pluralized lowercase name
# model:class = model resources being tested
# model_test_data:dict = dictionary for creating test models
# model_test_patch_data:dict = dictionary for updating models
# ##########################################################################


def create_nested_monster_routes_test(model_name, model, model_test_data, model_test_patch_data):

    class TestNestedMonsterModel:
        f""" [TESTING SUITE: <{model_name} routes>] """

        def test_get_resources_by_monster_id(self):
            f""" <GET /monsters/:id/{model_name}> retrieves a list of a monster's {model_name} """

            with app.app_context():
                db.create_all()

                m1 = Monster(**MONSTER_ONE)
                m2 = Monster(**MONSTER_TWO)

                db.session.add_all([m1, m2])
                db.session.commit()

                item1 = model(monster=m2, **model_test_data)
                item2 = model(monster=m2, **model_test_data)
                db.session.add_all([item1, item2])
                db.session.commit()

                res = app.test_client().get(f"/monsters/{m1.id}/{model_name.replace('_', '-')}")
                assert res.status_code == 200
                assert res.content_type == 'application/json'
                res_data = res.json
                assert len(res_data) == 0

                res = app.test_client().get(f"/monsters/{m2.id}/{model_name.replace('_', '-')}")
                assert res.status_code == 200
                assert res.content_type == 'application/json'
                res_data = res.json
                assert len(res_data) == 2

                assert item1.id == res_data[0]['id']
                assert item2.id == res_data[1]['id']

                db.session.remove()
                db.drop_all()

        
        def test_post_monster_accepts_nested_resources(self):
            f""" <POST /monsters> creates and returns a monster with nested {model_name} """

            with app.app_context():
                db.create_all()

                m1 = Monster(**MONSTER_ONE)
                m2 = Monster(**MONSTER_TWO)

                db.session.add_all([m1, m2])
                db.session.commit()

                MONSTER_DICT = {
                    'name': 'Test Monster',
                    'size': 'medium',
                    'category': 'humanoid',
                    model_name: [ model_test_data ]
                }

                res = app.test_client().post( '/monsters', json=MONSTER_DICT )
                assert res.status_code == 201

                res_data = res.json
                assert res_data['id']
                assert res_data[model_name]
                assert len(res_data[model_name]) == 1

                db_monster = Monster.query.all()[-1]
                db_data = model.query.where( model.monster_id == db_monster.id ).all()
                assert len(db_data) == 1

                db.session.remove()
                db.drop_all()
        
        def test_patch_monster_resource_by_id(self):
            f""" <PATCH /monsters/:monster_id/{model_name.replace('_', '-')}/:id> patches and returns an instance of a monster's {model_name} """
            
            with app.app_context():
                db.create_all()

                m1 = Monster(**MONSTER_ONE)
                m2 = Monster(**MONSTER_TWO)

                db.session.add_all([m1, m2])
                db.session.commit()
                MONSTER_DICT = {
                    'name': 'Test Monster',
                    'size': 'medium',
                    'category': 'humanoid',
                }

                NEW_M = Monster(**MONSTER_DICT)
                NEW_ITEM = model(monster=NEW_M, **model_test_data)

                db.session.add_all([NEW_M, NEW_ITEM])
                db.session.commit()

                res = app.test_client().patch( f"/monsters/{NEW_M.id}/{model_name.replace('_', '-')}/{NEW_ITEM.id}", json=model_test_patch_data )
                assert res.status_code == 202

                res_data = res.json
                for key in model_test_patch_data:
                    assert res_data[key] == model_test_patch_data[key]
                assert res_data['monster_id'] == NEW_M.id

                db.session.remove()
                db.drop_all()

        def test_patch_monster_resource_by_id_ignores_invalid_keys(self):
            f""" <PATCH /monsters/:monster_id/{model_name.replace('_', '-')}/:id> patches and returns {model_name} and also ignores invalid keys """

            with app.app_context():
                db.create_all()

                MONSTER_DICT = {
                    'name': 'Test Monster',
                    'size': 'medium',
                    'category': 'humanoid',
                }

                NEW_M = Monster(**MONSTER_DICT)
                NEW_ITEM = model(monster=NEW_M, **model_test_data)

                db.session.add_all([NEW_M, NEW_ITEM])
                db.session.commit()

                res = app.test_client().patch( f"/monsters/{NEW_M.id}/{model_name.replace('_', '-')}/{NEW_ITEM.id}", json={ **model_test_patch_data, 'thacko': 1234567890 } )
                assert res.status_code == 202

                res_data = res.json
                assert res_data['monster_id'] == NEW_M.id
                assert res_data.get('thacko') == None

                db.session.remove()
                db.drop_all()

        def test_delete_monster_resource_by_id(self):
            f""" <DELETE /monsters/:monster_id/{model_name.replace('_', '-')}/:id> deletes {model_name} by id and returns empty response """

            with app.app_context():
                db.create_all()

                MONSTER_DICT = {
                    'name': 'Test Monster',
                    'size': 'medium',
                    'category': 'humanoid',
                }

                NEW_M = Monster(**MONSTER_DICT)
                NEW_ITEM = model(monster=NEW_M, **model_test_data)

                db.session.add_all([NEW_M, NEW_ITEM])
                db.session.commit()

                assert len( model.query.where( model.monster_id == NEW_M.id ).all() ) == 1

                res = app.test_client().delete( f"/monsters/{NEW_M.id}/{model_name.replace('_', '-')}/{NEW_ITEM.id}" )
                assert res.status_code == 204

                assert len( model.query.where( model.monster_id == NEW_M.id ).all() ) == 0

                db.session.remove()
                db.drop_all()


    return TestNestedMonsterModel