import pytest

from models import db, Monster, Skill
from create_app import create_app
from testing.test_monsters import MONSTER_ONE, MONSTER_TWO

app = create_app('TESTING')

@pytest.fixture(autouse=True)
def run_before_and_after():
    with app.app_context():
        app.config.update({
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',
            'TESTING': True
        })
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