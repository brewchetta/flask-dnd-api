import pytest

from create_app import create_app
from models import db, Monster, ConditionImmunity
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


class TestConditionImmunity:
    """ [TESTING SUITE: <ConditionImmunity>] """

    def test_ConditionImmunity_has_attributes(self):
        """ (attributes) Has proper attributes """
        s = ConditionImmunity(condition_type="poisoned", monster_id=1)
        db.session.add(s)
        db.session.commit()

        db_item = ConditionImmunity.query.first()
        assert db_item
        assert db_item.condition_type == s.condition_type
        assert db_item.monster_id == 1

    def test_validates_condition_type(self):
        """ (validations) Validates ConditionImmunity condition_type """
        db_item = ConditionImmunity(condition_type="poisoned", monster_id=1)
        db.session.add(db_item)
        db.session.commit()

        assert db_item.id

        with pytest.raises(ValueError):
            db_item.condition_type = "insane in the membrane"
            db.session.commit()

    

    def test_belongs_to_monster(self):
        """ (assocations) Belongs to a monster """
        s = ConditionImmunity(condition_type="poisoned", monster_id=1)
        db.session.add(s)
        db.session.commit()

        db_item = ConditionImmunity.query.first()
        assert db_item
        assert db_item.monster
        assert db_item.monster.id == 1
