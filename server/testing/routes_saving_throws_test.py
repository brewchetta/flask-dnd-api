import pytest

from models import db, Monster, SavingThrow
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

class TestSavingThrowRoutes:
    """ [TESTING SUITE: <SavingThrow routes>] """

    def test_get_saving_throws_by_monster_id(self):
        """ <GET /monsters/:id/saving-throws> retrieves a list of a monster's saving throws """

        m1 = Monster.query.all()[0]
        m2 = Monster.query.all()[1]

        s1 = SavingThrow(name="dex", value=1, monster=m1)
        s2 = SavingThrow(name="int", value=2, monster=m1)
        s3 = SavingThrow(name="str", value=3, monster=m1)
        s4 = SavingThrow(name="con", value=10, monster=m2)
        db.session.add_all([s1, s2, s3, s4])
        db.session.commit()

        res = app.test_client().get(f"/monsters/{m1.id}/saving-throws")
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json

        assert len(res_data) == 3

        assert s1.id == res_data[0]['id']
        assert s1.value == res_data[0]['value']
        assert s1.name == res_data[0]['name']

        assert s2.id == res_data[1]['id']
        assert s2.value == res_data[1]['value']
        assert s2.name == res_data[1]['name']

    
    def test_post_monster_accepts_nested_saving_throws(self):
        """ <POST /monsters> creates and returns a monster with nested saving throws """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
            'saving_throws': [ { 'name': 'dex', 'value': 2 }, { 'name': 'str', 'value': 3 } ]
        }

        res = app.test_client().post( '/monsters', json=MONSTER_DICT )
        assert res.status_code == 201

        res_data = res.json
        assert res_data['id']
        assert res_data['saving_throws']
        assert len(res_data['saving_throws']) == 2

        monster = Monster.query.where( Monster.name == 'Test Monster' ).first()
        assert len(monster.saving_throws) == 2
    
    def test_patch_monster_saving_throw_by_id(self):
        """ <PATCH /monsters/:monster_id/saving-throws/:saving_throw_id> patches and returns a saving throw """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }

        NEW_M = Monster(**MONSTER_DICT)
        NEW_S = SavingThrow(name='dex', value=2, monster=NEW_M)

        db.session.add_all([NEW_M, NEW_S])
        db.session.commit()

        res = app.test_client().patch( f"/monsters/{NEW_M.id}/saving-throws/{NEW_S.id}", json={ 'name': 'wis', 'value': 10 } )
        assert res.status_code == 202

        res_data = res.json
        assert res_data['name'] == 'wis'
        assert res_data['value'] == 10
        assert res_data['monster_id'] == NEW_M.id

    def test_patch_monster_saving_throw_by_id_ignores_invalid_keys(self):
        """ <PATCH /monsters/:monster_id/saving-throws/:skill_id> patches and returns a saving throw and also ignores invalid keys """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }

        NEW_M = Monster(**MONSTER_DICT)
        NEW_S = SavingThrow(name='str', value=2, monster=NEW_M)

        db.session.add_all([NEW_M, NEW_S])
        db.session.commit()

        res = app.test_client().patch( f"/monsters/{NEW_M.id}/saving-throws/{NEW_S.id}", json={ 'name': 'int', 'value': 10, 'thacko': 1234567890 } )
        assert res.status_code == 202

        res_data = res.json
        assert res_data['name'] == 'int'
        assert res_data['value'] == 10
        assert res_data['monster_id'] == NEW_M.id
        assert res_data.get('thacko') == None

    def test_delete_monster_saving_throw_by_id(self):
        """ <DELETE /monsters/:monster_id/saving-throws/:saving_throw_id> deletes skill and returns empty response """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }

        NEW_M = Monster(**MONSTER_DICT)
        NEW_S = SavingThrow(name='dex', value=2, monster=NEW_M)

        db.session.add_all([NEW_M, NEW_S])
        db.session.commit()

        assert len(NEW_M.saving_throws) == 1

        res = app.test_client().delete( f"/monsters/{NEW_M.id}/saving-throws/{NEW_S.id}" )
        assert res.status_code == 204

        assert len(NEW_M.saving_throws) == 0