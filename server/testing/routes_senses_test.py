import pytest

from models import db, Monster, Sense
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

class TestSensesRoutes:
    """ [TESTING SUITE: <Sense routes>] """

    def test_get_senses_by_monster_id(self):
        """ <GET /monsters/:id/senses> retrieves a list of a monster's senses """

        m1 = Monster.query.all()[0]
        m2 = Monster.query.all()[1]

        s1 = Sense(name="darkvision", distance=60, monster=m2)
        s2 = Sense(name="blindsight", distance=10, monster=m2)
        db.session.add_all([s1, s2])
        db.session.commit()

        res = app.test_client().get(f"/monsters/{m1.id}/senses")
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert len(res_data) == 0

        res = app.test_client().get(f"/monsters/{m2.id}/senses")
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert len(res_data) == 2

        assert s1.id == res_data[0]['id']
        assert s1.distance == res_data[0]['distance']
        assert s1.name == res_data[0]['name']

        assert s2.id == res_data[1]['id']
        assert s2.distance == res_data[1]['distance']
        assert s2.name == res_data[1]['name']

    
    def test_post_monster_accepts_nested_senses(self):
        """ <POST /monsters> creates and returns a monster with nested senses """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
            'senses': [ { 'name': 'darkvision', 'distance': 60 }, { 'name': 'blindsight', 'distance': 120 } ]
        }

        res = app.test_client().post( '/monsters', json=MONSTER_DICT )
        assert res.status_code == 201

        res_data = res.json
        assert res_data['id']
        assert res_data['senses']
        assert len(res_data['senses']) == 2

        monster = Monster.query.where( Monster.name == 'Test Monster' ).first()
        assert len(monster.senses) == 2
    
    def test_patch_monster_sense_by_id(self):
        """ <PATCH /monsters/:monster_id/senses/:sense_id> patches and returns a sense """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }

        NEW_M = Monster(**MONSTER_DICT)
        NEW_S = Sense(name='darkvision', distance=60, monster=NEW_M)

        db.session.add_all([NEW_M, NEW_S])
        db.session.commit()

        res = app.test_client().patch( f"/monsters/{NEW_M.id}/senses/{NEW_S.id}", json={ 'name': 'blindsight', 'distance': 10 } )
        assert res.status_code == 202

        res_data = res.json
        assert res_data['name'] == 'blindsight'
        assert res_data['distance'] == 10
        assert res_data['monster_id'] == NEW_M.id

    def test_patch_monster_sense_by_id_ignores_invalid_keys(self):
        """ <PATCH /monsters/:monster_id/senses/:sense_id> patches and returns a skill and also ignores invalid keys """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }

        NEW_M = Monster(**MONSTER_DICT)
        NEW_S = Sense(name='history', distance=2, monster=NEW_M)

        db.session.add_all([NEW_M, NEW_S])
        db.session.commit()

        res = app.test_client().patch( f"/monsters/{NEW_M.id}/senses/{NEW_S.id}", json={ 'name': 'blindsight', 'distance': 10, 'thacko': 1234567890 } )
        assert res.status_code == 202

        res_data = res.json
        assert res_data['name'] == 'blindsight'
        assert res_data['distance'] == 10
        assert res_data['monster_id'] == NEW_M.id
        assert res_data.get('thacko') == None

    def test_delete_monster_sense_by_id(self):
        """ <DELETE /monsters/:monster_id/senses/:sense_id> deletes sense and returns empty response """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }

        NEW_M = Monster(**MONSTER_DICT)
        NEW_S = Sense(name='darkvision', distance=120, monster=NEW_M)

        db.session.add_all([NEW_M, NEW_S])
        db.session.commit()

        assert len(NEW_M.senses) == 1

        res = app.test_client().delete( f"/monsters/{NEW_M.id}/senses/{NEW_S.id}" )
        print(res)
        assert res.status_code == 204

        assert len(NEW_M.senses) == 0