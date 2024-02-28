import pytest

from create_app import create_app
from models import db, Monster, Skill
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
        m = Monster(**MONSTER_TWO)
        db.session.add(m)
        db.session.commit()

        old_category = m.category
        
        m.category = "celestial"
        db.session.commit()

        assert m.category != old_category
        assert m.category == "celestial"

        with pytest.raises(ValueError):
            m.category = "space alien"
            db.session.commit()

    def test_validates_armor_class(self):
        """ (validations) Validates armor_class to be above 0 """

        m = Monster(**MONSTER_TWO)
        db.session.add(m)
        db.session.commit()
        
        m.armor_class = 20
        db.session.commit()
        assert m.armor_class == 20

        with pytest.raises(ValueError):
            m.armor_class = -1
            db.session.commit()

    def test_validates_hit_points(self):
        """ (validations) Validates hit_points to be above 0 """

        m = Monster(**MONSTER_TWO)
        db.session.add(m)
        db.session.commit()
        
        m.hit_points = 20
        db.session.commit()
        assert m.hit_points == 20

        with pytest.raises(ValueError):
            m.hit_points = -1
            db.session.commit()


    def test_validates_hit_dice_count(self):
        """ (validations) Validates hit_dice_count to be above 0 """

        m = Monster(**MONSTER_TWO)
        db.session.add(m)
        db.session.commit()
        
        m.hit_dice_count = 20
        db.session.commit()
        assert m.hit_dice_count == 20

        with pytest.raises(ValueError):
            m.hit_dice_count = -1
            db.session.commit()


    def test_validates_challenge_rating(self):
        """ (validations) Validates challenge_rating to be above 0 """

        m = Monster(**MONSTER_TWO)
        db.session.add(m)
        db.session.commit()
        
        m.challenge_rating = 20
        db.session.commit()
        assert m.challenge_rating == 20

        with pytest.raises(ValueError):
            m.challenge_rating = -1
            db.session.commit()


    def test_validates_proficiency_bonus(self):
        """ (validations) Validates proficiency_bonus to be above 0 """

        m = Monster(**MONSTER_TWO)
        db.session.add(m)
        db.session.commit()
        
        m.proficiency_bonus = 20
        db.session.commit()
        assert m.proficiency_bonus == 20

        with pytest.raises(ValueError):
            m.proficiency_bonus = -1
            db.session.commit()

    def test_validates_hit_dice_size(self):
        """ (validations) Validates hit_dice_size to be only certain values """

        m = Monster(**MONSTER_TWO)
        db.session.add(m)
        db.session.commit()
        
        m.hit_dice_size = 12
        db.session.commit()
        assert m.hit_dice_size == 12

        with pytest.raises(ValueError):
            m.hit_dice_size = 11
            db.session.commit()


    def test_validates_ability_scores(self):
        """ (validations) Validates ability scores (strength, dexterity, constitution, intelligence, wisdom, charisma) within proper values """

        m = Monster(**MONSTER_TWO)
        db.session.add(m)
        db.session.commit()
        
        m.strength = 14
        db.session.commit()
        assert m.strength == 14
        
        with pytest.raises(ValueError):
            m.strength = 31
            db.session.commit()

        m.dexterity = 14
        db.session.commit()
        assert m.dexterity == 14
        
        with pytest.raises(ValueError):
            m.dexterity = 31
            db.session.commit()

        m.constitution = 14
        db.session.commit()
        assert m.constitution == 14
        
        with pytest.raises(ValueError):
            m.constitution = 31
            db.session.commit()

        m.intelligence = 14
        db.session.commit()
        assert m.intelligence == 14
        
        with pytest.raises(ValueError):
            m.intelligence = 31
            db.session.commit()

        m.wisdom = 14
        db.session.commit()
        assert m.wisdom == 14
        
        with pytest.raises(ValueError):
            m.wisdom = 31
            db.session.commit()

        m.charisma = 14
        db.session.commit()
        assert m.charisma == 14
        
        with pytest.raises(ValueError):
            m.charisma = 31
            db.session.commit()

    def test_validates_spell_slots(self):
        """ (validations) Validates spell slots to be within proper values """

        m = Monster(**MONSTER_TWO)
        db.session.add(m)
        db.session.commit()
        
        m.spell_slots_first_level = 0
        db.session.commit()
        assert m.spell_slots_first_level == 0
        with pytest.raises(ValueError):
            m.spell_slots_first_level = -1
            db.session.commit()
        with pytest.raises(ValueError):
            m.spell_slots_first_level = 5
            db.session.commit()

        m.spell_slots_second_level = 1
        db.session.commit()
        assert m.spell_slots_second_level == 1
        with pytest.raises(ValueError):
            m.spell_slots_second_level = -1
            db.session.commit()

        m.spell_slots_third_level = 2
        db.session.commit()
        assert m.spell_slots_third_level == 2
        with pytest.raises(ValueError):
            m.spell_slots_third_level = 5
            db.session.commit()

        m.spell_slots_fourth_level = 3
        db.session.commit()
        assert m.spell_slots_fourth_level == 3
        with pytest.raises(ValueError):
            m.spell_slots_fourth_level = -1
            db.session.commit()

        m.spell_slots_fifth_level = 4
        db.session.commit()
        assert m.spell_slots_fifth_level == 4
        with pytest.raises(ValueError):
            m.spell_slots_fifth_level = 5
            db.session.commit()

        m.spell_slots_sixth_level = 4
        db.session.commit()
        assert m.spell_slots_sixth_level == 4
        with pytest.raises(ValueError):
            m.spell_slots_sixth_level = 5
            db.session.commit()

        m.spell_slots_seventh_level = 4
        db.session.commit()
        assert m.spell_slots_seventh_level == 4
        with pytest.raises(ValueError):
            m.spell_slots_seventh_level = 5
            db.session.commit()

        m.spell_slots_eighth_level = 4
        db.session.commit()
        assert m.spell_slots_eighth_level == 4
        with pytest.raises(ValueError):
            m.spell_slots_eighth_level = 5
            db.session.commit()

        m.spell_slots_ninth_level = 4
        db.session.commit()
        assert m.spell_slots_ninth_level == 4
        with pytest.raises(ValueError):
            m.spell_slots_ninth_level = 5
            db.session.commit()

    def test_has_many_skills(self):
        """ (associations) Can have many associated skills """

        m = Monster(**MONSTER_ONE)
        db.session.add(m)
        db.session.commit()

        s1 = Skill(name="history", value="2", monster_id=m.id)
        s2 = Skill(name="arcana", value="2", monster_id=m.id)
        s3 = Skill(name="perception", value="2", monster_id=m.id)
        db.session.add_all([s1, s2, s3])
        db.session.commit()

        assert len(m.skills) == 3


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