import pytest

from create_app import create_app
from models import db, Monster, SavingThrow
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


class TestSavingThrow:
    """ [TESTING SUITE: <SAVING_THROW>] """

    def test_has_attributes(self):
        """ (attributes) Has proper attributes """
        s = SavingThrow(name="dex", value="2", monster_id=1)
        db.session.add(s)
        db.session.commit()

        db_skill = SavingThrow.query.first()
        assert db_skill
        assert db_skill.name == s.name
        assert db_skill.value == s.value
        assert db_skill.monster_id == 1

    def test_validates_aving_throw_name(self):
        """ (validations) Validates saving throw name """
        s = SavingThrow(name="intelligence", value="2", monster_id=1)
        db.session.add(s)
        db.session.commit()

        assert s.id
        assert s.name == 'int'

        with pytest.raises(ValueError):
            s.name = "craziness"
            db.session.commit()

        with pytest.raises(ValueError):
            s2 = SavingThrow(name="hunger", value=3)
            db.session.add(s2)
            db.session.commit()

    def test_belongs_to_monster(self):
        """ (assocations) Belongs to a monster """
        s = SavingThrow(name="dex", value="2", monster_id=1)
        db.session.add(s)
        db.session.commit()

        db_saving_throw = SavingThrow.query.first()
        assert db_saving_throw
        assert db_saving_throw.monster
        assert db_saving_throw.monster.id == 1