import pytest

from create_app import create_app
from models import db, Monster, Language
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


class TestLanguage:
    """ [TESTING SUITE: <Language>] """

    def test_Language_has_attributes(self):
        """ (attributes) Has proper attributes """
        s = Language(name="sylvan", monster_id=1)
        db.session.add(s)
        db.session.commit()

        db_item = Language.query.first()
        assert db_item
        assert db_item.name == s.name
        assert db_item.monster_id == 1



    def test_belongs_to_monster(self):
        """ (assocations) Belongs to a monster """
        s = Language(name="sylvan", monster_id=1)
        db.session.add(s)
        db.session.commit()

        db_item = Language.query.first()
        assert db_item
        assert db_item.monster
        assert db_item.monster.id == 1
