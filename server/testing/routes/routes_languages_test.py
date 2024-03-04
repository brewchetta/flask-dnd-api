
import pytest
from create_app import create_app
from models import db, Monster, Language
from testing.test_monsters import MONSTER_ONE, MONSTER_TWO

app = create_app('TESTING')

class TestNestedMonsterModel:
    """ [TESTING SUITE: <languages routes>] """

    def test_get_resources_by_monster_id(self):
        """ <GET /monsters/:id/languages> retrieves a list of a monster's languages """

        with app.app_context():
            db.create_all()

            m1 = Monster(**MONSTER_ONE)
            m2 = Monster(**MONSTER_TWO)

            db.session.add_all([m1, m2])
            db.session.commit()

            item1 = Language(monster=m2, **{'name': 'sylvan'})
            item2 = Language(monster=m2, **{'name': 'sylvan'})
            db.session.add_all([item1, item2])
            db.session.commit()

            res = app.test_client().get(f"/monsters/{m1.id}/languages")
            assert res.status_code == 200
            assert res.content_type == 'application/json'
            res_data = res.json
            assert len(res_data) == 0

            res = app.test_client().get(f"/monsters/{m2.id}/languages")
            assert res.status_code == 200
            assert res.content_type == 'application/json'
            res_data = res.json
            assert len(res_data) == 2

            assert item1.id == res_data[0]['id']
            assert item2.id == res_data[1]['id']

            db.session.remove()
            db.drop_all()

    
    def test_post_monster_accepts_nested_resources(self):
        """ <POST /monsters> creates and returns a monster with nested languages """

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
                'languages': [ {'name': 'sylvan'} ]
            }

            res = app.test_client().post( '/monsters', json=MONSTER_DICT )
            assert res.status_code == 201

            res_data = res.json
            assert res_data['id']
            assert res_data['languages']
            assert len(res_data['languages']) == 1

            db_monster = Monster.query.all()[-1]
            db_data = Language.query.where( Language.monster_id == db_monster.id ).all()
            assert len(db_data) == 1

            db.session.remove()
            db.drop_all()
    
    def test_patch_monster_resource_by_id(self):
        """ <PATCH /monsters/:monster_id/languages/:id> patches and returns an instance of a monster's languages """
        
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
            NEW_ITEM = Language(monster=NEW_M, **{'name': 'sylvan'})

            db.session.add_all([NEW_M, NEW_ITEM])
            db.session.commit()

            res = app.test_client().patch( f"/monsters/{NEW_M.id}/languages/{NEW_ITEM.id}", json={'name': 'infernal'} )
            assert res.status_code == 202

            res_data = res.json
            for key in {'name': 'infernal'}:
                assert res_data[key] == {'name': 'infernal'}[key]
            assert res_data['monster_id'] == NEW_M.id

            db.session.remove()
            db.drop_all()

    def test_patch_monster_resource_by_id_ignores_invalid_keys(self):
        """ <PATCH /monsters/:monster_id/languages/:id> patches and returns languages and also ignores invalid keys """

        with app.app_context():
            db.create_all()

            MONSTER_DICT = {
                'name': 'Test Monster',
                'size': 'medium',
                'category': 'humanoid',
            }

            NEW_M = Monster(**MONSTER_DICT)
            NEW_ITEM = Language(monster=NEW_M, **{'name': 'sylvan'})

            db.session.add_all([NEW_M, NEW_ITEM])
            db.session.commit()

            res = app.test_client().patch( f"/monsters/{NEW_M.id}/languages/{NEW_ITEM.id}", json={ **{'name': 'infernal'}, 'thacko': 1234567890 } )
            assert res.status_code == 202

            res_data = res.json
            assert res_data['monster_id'] == NEW_M.id
            assert res_data.get('thacko') == None

            db.session.remove()
            db.drop_all()

    def test_delete_monster_resource_by_id(self):
        """ <DELETE /monsters/:monster_id/languages/:id> deletes languages by id and returns empty response """

        with app.app_context():
            db.create_all()

            MONSTER_DICT = {
                'name': 'Test Monster',
                'size': 'medium',
                'category': 'humanoid',
            }

            NEW_M = Monster(**MONSTER_DICT)
            NEW_ITEM = Language(monster=NEW_M, **{'name': 'sylvan'})

            db.session.add_all([NEW_M, NEW_ITEM])
            db.session.commit()

            assert len( Language.query.where( Language.monster_id == NEW_M.id ).all() ) == 1

            res = app.test_client().delete( f"/monsters/{NEW_M.id}/languages/{NEW_ITEM.id}" )
            assert res.status_code == 204

            assert len( Language.query.where( Language.monster_id == NEW_M.id ).all() ) == 0

            db.session.remove()
            db.drop_all()
