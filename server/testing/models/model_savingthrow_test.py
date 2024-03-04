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
    """ [TESTING SUITE: <SavingThrow>] """

    def test_SavingThrow_has_attributes(self):
        """ (attributes) Has proper attributes """
        s = SavingThrow(name="dex", value="2", monster_id=1)
        db.session.add(s)
        db.session.commit()

        db_item = SavingThrow.query.first()
        assert db_item
        assert db_item.name == s.name
        assert db_item.value == s.value
        assert db_item.monster_id == 1

    def test_validates_name(self):
        """ (validations) Validates SavingThrow name """
        db_item = SavingThrow(name="dex", value="2", monster_id=1)
        db.session.add(db_item)
        db.session.commit()

        assert db_item.id

        with pytest.raises(ValueError):
            db_item.name = "charm"
            db.session.commit()

    

    def test_belongs_to_monster(self):
        """ (assocations) Belongs to a monster """
        s = SavingThrow(name="dex", value="2", monster_id=1)
        db.session.add(s)
        db.session.commit()

        db_item = SavingThrow.query.first()
        assert db_item
        assert db_item.monster
        assert db_item.monster.id == 1
