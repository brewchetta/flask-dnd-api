import pytest

from models import db, Monster, Spell, MonsterSpell
from create_app import create_app
from testing.test_monsters import MONSTER_ONE, MONSTER_TWO, MONSTER_THREE, MONSTER_FOUR, MONSTER_FIVE
from testing.test_spells import SPELL_ONE, SPELL_TWO, SPELL_THREE, SPELL_FOUR

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
            Spell(**SPELL_ONE),
            Spell(**SPELL_TWO),
            Spell(**SPELL_THREE),
            Spell(**SPELL_FOUR)
        ])

        yield

        db.session.remove()
        db.drop_all()

class TestMonsterSpellRoutes:
    """ [TESTING SUITE: <MonsterSpell routes>] """

    def test_get_monster_spells(self):
        """ <GET /monsters/:id> returns a nested list of spells associated with the monster """

        m = Monster.query.first()
        spells = Spell.query.all()

        db.session.add_all([
            MonsterSpell(monster=m, spell=spells[0]), 
            MonsterSpell(monster=m, spell=spells[1]), 
            MonsterSpell(monster=m, spell=spells[2]), 
            MonsterSpell(monster=m, spell=spells[3])
        ])
        db.session.commit()

        assert len(m.spells) == 4

        res = app.test_client().get(f'/monsters/{m.id}')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert res_data.get('spells')
        assert len(res_data['spells']) == 4

    def test_post_monster_accepts_nested_spell_names(self):
        """ <POST /monsters> creates and returns new monster with associated spells """

        m = Monster.query.first()
        sp = Spell.query.first()

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
            'spells': ["mage hand", "acid arrow"]
        }

        res = app.test_client().post( f'/monsters', json=MONSTER_DICT )
        assert res.status_code == 201
        res_data = res.json
        assert res_data['id']
        assert len(res_data['spells']) == 2
        assert res_data['spells'][0]['name'].lower() == 'mage hand'

    def test_post_monster_spells(self):
        """ <POST /monsters/:id/spells> associates and returns the associated spell """

        m = Monster.query.first()
        sp = Spell.query.where(Spell.name.ilike('mage hand')).first()

        S_DICT = { 'name': 'mage hand' }

        res = app.test_client().post( f'/monsters/{m.id}/spells', json=S_DICT )
        assert res.status_code == 201

        res_data = res.json
        assert res_data['id']
        assert res_data['name'].lower() == 'mage hand'
        assert sp in m.spells

    def test_post_monster_spells_returns_not_found_for_monster_or_spell(self):
        """ <POST /monsters/:id/monster-spells> creates and returns an error response if invalid """

        s = Spell.query.first()
        m = Monster.query.first()

        MS_DICT_ONE = { 'spell_id': 0 }
        MS_DICT_TWO = { 'spell_id': s.id }

        res = app.test_client().post( f'/monsters/{m.id}/monster-spells', json=MS_DICT_ONE )
        assert res.status_code == 404

        res = app.test_client().post( f'/monsters/0/monster-spells', json=MS_DICT_TWO )
        assert res.status_code == 404

    def test_patch_monster_with_spells_replaces_spells(self):
        """ <PATCH /monsters/:id> replaces existing monster spells """

        m = Monster.query.first()
        spells = Spell.query.all()

        db.session.add_all([
            MonsterSpell(monster=m, spell=spells[0]), 
            MonsterSpell(monster=m, spell=spells[1])
        ])
        db.session.commit()

        assert spells[0] in m.spells
        assert spells[2] not in m.spells

        res = app.test_client().patch( 
            f"/monsters/{m.id}", 
            json={"spells": [spells[2].name, spells[3].name]} 
        )
        assert res.status_code == 202

        res_data = res.json
        assert res_data['id'] == m.id
        assert res_data['spells']
        assert spells[0] not in m.spells
        assert spells[2] in m.spells        
    
    def test_delete_monster_spell_by_id(self):
        """ <DELETE /monsters/:monster_id/spell/:spell_id> deletes a monster spell association by id and returns a 204 No Content """

        m = Monster.query.first()
        s = Spell.query.first()
        ms = MonsterSpell(monster=m, spell=s)
        db.session.add(ms)
        db.session.commit()

        res = app.test_client().delete(f'/monsters/{m.id}/spells/{s.id}')
        assert res.status_code == 204

        assert len(m.monster_spells) == 0
        assert len(m.spells) == 0

    def test_delete_invalid_monster_by_id(self):
        """ <DELETE /monsters/:monster_id/spells/:spell_id> returns a 404 error if no monster or monster_spell found """

        m = Monster.query.first()
        s = Spell.query.first()
        ms = MonsterSpell(monster=m, spell=s)
        db.session.add(ms)
        db.session.commit()

        res = app.test_client().delete(f'/monsters/{m.id}/spells/0')
        assert res.status_code == 404
        res_data = res.json
        assert res_data['error']

        res = app.test_client().delete(f'/monsters/0/spells/{s.id}')
        assert res.status_code == 404
        res_data = res.json
        print(res_data)
        print(res)
        assert res_data['error']