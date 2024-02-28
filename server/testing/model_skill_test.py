import pytest

from create_app import create_app
from models import db, Monster, Skill
from testing.test_monsters import MONSTER_ONE

app = create_app('TESTING')

@pytest.fixture(autouse=True)
def run_before_and_after():
    with app.app_context():
        db.create_all()

        test_monster = Monster(**MONSTER_ONE)

        db.session.add(test_monster)
        db.session.commit()

        yield

        db.session.remove()
        db.drop_all()


class TestSkill:
    """ [TESTING SUITE: <Skill>] """

    def test_has_attributes(self):
        """ (attributes) Has proper attributes """
        s = Skill(name="history", value="2", monster_id=1)
        db.session.add(s)
        db.session.commit()

        db_skill = Skill.query.first()
        assert db_skill
        assert db_skill.name == s.name
        assert db_skill.value == s.value
        assert db_skill.monster_id == 1

    def test_validates_skill_name(self):
        """ (validations) Validates skill name """
        s = Skill(name="history", value="2", monster_id=1)
        db.session.add(s)
        db.session.commit()

        assert s.id

        with pytest.raises(ValueError):
            s.name = "crocheting"
            db.session.commit()

        with pytest.raises(ValueError):
            s2 = Skill(name="cross country skiing", value=3)
            db.session.add(s2)
            db.session.commit()

    def test_validates_skill_name(self):
        """ (validations) Properly cases skill name as part of validation """
        s = Skill(name="AnImAl HaNdLiNg", value="2", monster_id=1)
        db.session.add(s)
        db.session.commit()

        assert s.name == "animal handling"


    def test_belongs_to_monster(self):
        """ (assocations) Belongs to a monster """
        s = Skill(name="history", value="2", monster_id=1)
        db.session.add(s)
        db.session.commit()

        db_skill = Skill.query.first()
        assert db_skill
        assert db_skill.monster
        assert db_skill.monster.id == 1