import pytest

from create_app import create_app
from models import db, Monster
from testing.test_monsters import MONSTER_ONE, MONSTER_TWO, MONSTER_THREE, MONSTER_FOUR, MONSTER_FIVE

app = create_app('TESTING')

@pytest.fixture(autouse=True)
def run_before_and_after():
    with app.app_context():
        db.create_all()

        yield

        db.session.remove()
        db.drop_all()

class TestMonster:
    """ [TESTING SUITE: <Monster>] """

    def test_has_attributes(self):
        """ (attributes) Can include all proper attributes """
        m = Monster(**MONSTER_TWO)
        db.session.add(m)
        db.session.commit()

        db_monster = Monster.query.where(Monster.name == m.name).first()
        assert db_monster
        assert db_monster.name == m.name
        assert db_monster.dexterity == m.dexterity
        assert db_monster.spell_save_dc == m.spell_save_dc


    def test_validates_category(self):
        """ (validations) Validates category to be within certain values list """

    def test_validates_armor_class(self):
        """ (validations) Validates armor_class to be above 0 """

    def test_validates_hit_points(self):
        """ (validations) Validates hit_points to be above 0 """

    def test_validates_hit_dice_count(self):
        """ (validations) Validates hit_dice_count to be above 0 """

    def test_validates_challenge_rating(self):
        """ (validations) Validates challenge_rating to be above 0 """

    def test_validates_proficiency_bonus(self):
        """ (validations) Validates proficiency_bonus to be above 0 """

    def test_validates_hit_dice_size(self):
        """ (validations) Validates hit_dice_size to be only certain values """

    def test_validates_ability_scores(self):
        """ (validations) Validates ability scores (strength, dexterity, constitution, intelligence, wisdom, charisma) within proper values """


    def test_has_many_skills(self):
        """ (associations) Can have many associated skills """

    def test_has_many_saving_throws(self):
        """ (associations) Can have many associated saving_throws """

    def test_has_many_special_abilities(self):
        """ (associations) Can have many associated special_abilities """

    def test_has_many_senses(self):
        """ (associations) Can have many associated senses """

    def test_has_many_languages(self):
        """ (associations) Can have many associated languages """

    def test_has_many_actions(self):
        """ (associations) Can have many associated actions """

    def test_has_many_spells(self):
        """ (associations) Can have many associated monster_spells """

    def test_has_many_monster_spells(self):
        """ (associations) Can have many associated spells through monster_spells """