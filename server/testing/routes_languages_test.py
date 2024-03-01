import pytest

from models import db, Monster, Language
from create_app import create_app
from testing.test_monsters import MONSTER_ONE, MONSTER_TWO

app = create_app('TESTING')

@pytest.fixture(autouse=True)
def run_before_and_after():
    with app.app_context():
        db.create_all()

        db.session.add_all([
            Monster(**MONSTER_ONE),
            Monster(**MONSTER_TWO)
        ])
        db.session.commit()

        yield

        db.session.remove()
        db.drop_all()

class TestLanguagesRoutes:
    """ [TESTING SUITE: <Language routes>] """

    def test_get_languages_by_monster_id(self):
        """ <GET /monsters/:id/languages> retrieves a list of a monster's languages """

        m1 = Monster.query.all()[0]
        m2 = Monster.query.all()[1]

        s1 = Language(name="infernal", monster=m2)
        s2 = Language(name="sylvan", monster=m2)
        db.session.add_all([s1, s2])
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

        assert s1.id == res_data[0]['id']
        assert s1.name == res_data[0]['name']

        assert s2.id == res_data[1]['id']
        assert s2.name == res_data[1]['name']

    
    def test_post_monster_accepts_nested_languages(self):
        """ <POST /monsters> creates and returns a monster with nested languages """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
            'languages': [ { 'name': 'infernal' }, { 'name': 'sylvan' } ]
        }

        res = app.test_client().post( '/monsters', json=MONSTER_DICT )
        assert res.status_code == 201

        res_data = res.json
        assert res_data['id']
        assert res_data['languages']
        assert len(res_data['languages']) == 2

        monster = Monster.query.where( Monster.name == 'Test Monster' ).first()
        assert len(monster.languages) == 2
    
    def test_patch_monster_language_by_id(self):
        """ <PATCH /monsters/:monster_id/languages/:language_id> patches and returns a language """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }

        NEW_M = Monster(**MONSTER_DICT)
        NEW_S = Language(name='infernal', monster=NEW_M)

        db.session.add_all([NEW_M, NEW_S])
        db.session.commit()

        res = app.test_client().patch( f"/monsters/{NEW_M.id}/languages/{NEW_S.id}", json={ 'name': 'sylvan' } )
        assert res.status_code == 202

        res_data = res.json
        assert res_data['name'] == 'sylvan'
        assert res_data['monster_id'] == NEW_M.id

    def test_patch_monster_language_by_id_ignores_invalid_keys(self):
        """ <PATCH /monsters/:monster_id/languages/:language_id> patches and returns a skill and also ignores invalid keys """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }

        NEW_M = Monster(**MONSTER_DICT)
        NEW_S = Language(name='history', monster=NEW_M)

        db.session.add_all([NEW_M, NEW_S])
        db.session.commit()

        res = app.test_client().patch( f"/monsters/{NEW_M.id}/languages/{NEW_S.id}", json={ 'name': 'sylvan', 'thacko': 1234567890 } )
        assert res.status_code == 202

        res_data = res.json
        assert res_data['name'] == 'sylvan'
        assert res_data['monster_id'] == NEW_M.id
        assert res_data.get('thacko') == None

    def test_delete_monster_language_by_id(self):
        """ <DELETE /monsters/:monster_id/languages/:language_id> deletes language and returns empty response """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }

        NEW_M = Monster(**MONSTER_DICT)
        NEW_S = Language(name='infernal', monster=NEW_M)

        db.session.add_all([NEW_M, NEW_S])
        db.session.commit()

        assert len(NEW_M.languages) == 1

        res = app.test_client().delete( f"/monsters/{NEW_M.id}/languages/{NEW_S.id}" )
        print(res)
        assert res.status_code == 204

        assert len(NEW_M.languages) == 0