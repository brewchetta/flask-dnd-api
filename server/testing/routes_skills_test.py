import pytest

from models import db, Monster, Skill
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

class TestSkillRoutes:
    """ [TESTING SUITE: <Skill routes>] """

    def test_get_skills_by_monster_id(self):
        """ <GET /monsters/:id/skills> retrieves a list of a monster's skills """

        m1 = Monster.query.all()[0]
        m2 = Monster.query.all()[1]

        s1 = Skill(name="history", value=1, monster=m1)
        s2 = Skill(name="perception", value=2, monster=m1)
        s3 = Skill(name="arcana", value=3, monster=m1)
        s4 = Skill(name="arcana", value=10, monster=m2)
        db.session.add_all([s1, s2, s3, s4])
        db.session.commit()

        res = app.test_client().get(f"/monsters/{m1.id}/skills")
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

    
    def test_post_monster_accepts_nested_skills(self):
        """ <POST /monsters> creates and returns a monster with nested skills """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
            'skills': [ { 'name': 'history', 'value': 2 }, { 'name': 'arcana', 'value': 3 } ]
        }

        res = app.test_client().post( '/monsters', json=MONSTER_DICT )
        assert res.status_code == 201

        res_data = res.json
        assert res_data['id']
        assert res_data['skills']
        assert len(res_data['skills']) == 2

        monster = Monster.query.where( Monster.name == 'Test Monster' ).first()
        assert len(monster.skills) == 2
    
    def test_patch_monster_skill_by_id(self):
        """ <PATCH /monsters/:monster_id/skills/:skill_id> patches and returns a skill """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }

        NEW_M = Monster(**MONSTER_DICT)
        NEW_S = Skill(name='history', value=2, monster=NEW_M)

        db.session.add_all([NEW_M, NEW_S])
        db.session.commit()

        res = app.test_client().patch( f"/monsters/{NEW_M.id}/skills/{NEW_S.id}", json={ 'name': 'athletics', 'value': 10 } )
        assert res.status_code == 202

        res_data = res.json
        assert res_data['name'] == 'athletics'
        assert res_data['value'] == 10
        assert res_data['monster_id'] == NEW_M.id

    def test_patch_monster_skill_by_id_ignores_invalid_keys(self):
        """ <PATCH /monsters/:monster_id/skills/:skill_id> patches and returns a skill and also ignores invalid keys """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }

        NEW_M = Monster(**MONSTER_DICT)
        NEW_S = Skill(name='history', value=2, monster=NEW_M)

        db.session.add_all([NEW_M, NEW_S])
        db.session.commit()

        res = app.test_client().patch( f"/monsters/{NEW_M.id}/skills/{NEW_S.id}", json={ 'name': 'athletics', 'value': 10, 'thacko': 1234567890 } )
        assert res.status_code == 202

        res_data = res.json
        assert res_data['name'] == 'athletics'
        assert res_data['value'] == 10
        assert res_data['monster_id'] == NEW_M.id
        assert res_data.get('thacko') == None

    def test_delete_monster_skill_by_id(self):
        """ <DELETE /monsters/:monster_id/skills/:skill_id> deletes skill and returns empty response """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }

        NEW_M = Monster(**MONSTER_DICT)
        NEW_S = Skill(name='history', value=2, monster=NEW_M)

        db.session.add_all([NEW_M, NEW_S])
        db.session.commit()

        assert len(NEW_M.skills) == 1

        res = app.test_client().delete( f"/monsters/{NEW_M.id}/skills/{NEW_S.id}" )
        assert res.status_code == 204

        assert len(NEW_M.skills) == 0