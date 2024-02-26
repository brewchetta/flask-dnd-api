import pytest
from models import Monster
from app import app, db
from testing.test_monsters import MONSTER_ONE, MONSTER_TWO, MONSTER_THREE, MONSTER_FOUR, MONSTER_FIVE

MONSTER_ONE = {
    "name": "Monday Devil",
    "size": "medium",
    "category": "fiend",
    "armor_class": 10,
    "hit_points": 10,
    "hit_dice_count": 10,
    "hit_dice_size": 10,
    "strength": 10,
    "dexterity": 10,
    "constitution": 10,
    "intelligence": 10,
    "wisdom": 10,
    "charisma": 10,
    "challenge_rating": 10,
    "proficiency_bonus": 2,
    "spellcasting_level": 0,
    "spellcasting_ability": None,
    "spell_save_dc": 0,
    "spell_modifier": 0
}

MONSTER_TWO = {
    "name": "Tuesday Wizard Lizard",
    "size": "medium",
    "category": "humanoid",
    "sub_category": "dragonborn",
    "armor_class": 10,
    "hit_points": 10,
    "hit_dice_count": 10,
    "hit_dice_size": 10,
    "strength": 10,
    "dexterity": 10,
    "constitution": 10,
    "intelligence": 20,
    "wisdom": 10,
    "charisma": 10,
    "challenge_rating": 10,
    "proficiency_bonus": 2,
    "spellcasting_level": 3,
    "spellcasting_ability": "intelligence",
    "spell_save_dc": 12,
    "spell_modifier": 3,
    "spell_slots_first_level": 3,
    "spell_slots_second_level": 2
}

@pytest.fixture(autouse=True)
def run_before_and_after():
    with app.app_context():
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        db.create_all()

        yield

        db.session.remove()
        db.drop_all()

class TestRoutes:
    """ [TESTING SUITE: <routes>] """

    def test_get_monsters(self):
        """ <GET /monsters> retrieves a list of monsters """

        print(app.config['SQLALCHEMY_DATABASE_URI'])

        db.session.add_all([Monster(**MONSTER_ONE), Monster(**MONSTER_TWO)])
        db.session.commit()

        res = app.test_client().get('/monsters')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        monsters = Monster.query.all()
        assert [m.id for m in monsters] == [ m['id'] for m in res_data ]
        assert [m.name for m in monsters] == [ m['name'] for m in res_data ]

    def test_post_monster(self):
        """ <POST /monsters> creates and returns new monster """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }

        res = app.test_client().post( '/monsters', json=MONSTER_DICT )
        assert res.status_code == 201

        res_data = res.json
        assert res_data['id']
        assert res_data['name'] == 'Test Monster'

        monster = Monster.query.where( Monster.name == 'Test Monster' ).first()
        assert monster