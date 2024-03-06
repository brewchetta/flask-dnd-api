import pytest

from models import db, Spell
from create_app import create_app
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

        yield

        db.session.remove()
        db.drop_all()

class TestSpellRoutes:
    """ [TESTING SUITE: <Spell routes>] """

    def test_get_spells(self):
        """ <GET /spells> retrieves a list of spells """

        db.session.add_all([
            Spell(**SPELL_ONE), 
            Spell(**SPELL_TWO), 
            Spell(**SPELL_THREE), 
        ])
        db.session.commit()

        res = app.test_client().get('/spells')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        spells = Spell.query.all()
        assert [s.id for s in spells] == [ s['id'] for s in res_data ]
        assert [s.name for s in spells] == [ s['name'] for s in res_data ]

    def test_get_spells_with_page(self):
        """ <GET /spells?page=:int> retrieves a list of spells offset by a page query defaulting at 10 spells per page """

        sp_list = []
        for n in range(50):
            if n == 0:
                sp_list.append(Spell(**SPELL_ONE))
            elif n == 10:
                sp_list.append(Spell(**SPELL_TWO))
            elif n == 20:
                sp_list.append(Spell(**SPELL_THREE))
            else:
                sp_list.append(Spell(**SPELL_FOUR))

        db.session.add_all(sp_list)
        db.session.commit()

        res = app.test_client().get('/spells?page=1')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert len(res_data) == 10
        assert res_data[0]['name'] == SPELL_ONE['name']

        res = app.test_client().get('/spells?page=2')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert len(res_data) == 10
        assert res_data[0]['name'] == SPELL_TWO['name']

        res = app.test_client().get('/spells?page=3')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert len(res_data) == 10
        assert res_data[0]['name'] == SPELL_THREE['name']

    def test_get_spells_with_page_count(self):
        """ <GET /spells?page_count=:int> retrieves a list of spells of a certain number on a page """

        sp_list = []
        for n in range(50):
            if n == 0:
                sp_list.append(Spell(**SPELL_ONE))
            elif n == 4:
                sp_list.append(Spell(**SPELL_TWO))
            elif n == 7:
                sp_list.append(Spell(**SPELL_THREE))
            else:
                sp_list.append(Spell(**SPELL_FOUR))

        db.session.add_all(sp_list)
        db.session.commit()

        res = app.test_client().get('/spells?page_count=5')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert len(res_data) == 5
        assert res_data[0]['name'] == SPELL_ONE['name']
        assert res_data[4]['name'] == SPELL_TWO['name']

        res = app.test_client().get('/spells?page_count=8')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert len(res_data) == 8
        assert res_data[0]['name'] == SPELL_ONE['name']
        assert res_data[7]['name'] == SPELL_THREE['name']

    def test_get_spells_with_page_and_page_count(self):
        """ <GET /spells?page_count=:int&page=:int> retrieves a list of spells of a certain number offset by a number of pages """

        mon_list = []
        for n in range(50):
            if n == 5:
                mon_list.append(Spell(**SPELL_TWO))
            elif n == 9:
                mon_list.append(Spell(**SPELL_THREE))
            else:
                mon_list.append(Spell(**SPELL_FOUR))

        db.session.add_all(mon_list)
        db.session.commit()

        res = app.test_client().get('/spells?page_count=5&page=2')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert len(res_data) == 5
        assert res_data[0]['name'] == SPELL_TWO['name']
        assert res_data[4]['name'] == SPELL_THREE['name']

    def test_get_spells_by_name(self):
        """ <GET /spells> accepts a 'name' query that returns based on name """

        db.session.add_all([Spell(**SPELL_ONE), Spell(**SPELL_TWO), Spell(**SPELL_THREE), Spell(**SPELL_FOUR)])
        db.session.commit()

        res = app.test_client().get('/spells?name=mage')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        spells = Spell.query.where(Spell.name.like("%mage%")).all()
        assert [s.id for s in spells] == [ s['id'] for s in res_data ]
        assert [s.name for s in spells] == [ s['name'] for s in res_data ]
        assert len(res_data) < len(Spell.query.all())

    def test_get_spells_by_school(self):
        """ <GET /spells> accepts a 'school' query that returns based on spell school """

        db.session.add_all([
            Spell(**SPELL_ONE), 
            Spell(**SPELL_TWO), 
            Spell(**SPELL_THREE), 
            Spell(**SPELL_FOUR)
        ])
        db.session.commit()

        res = app.test_client().get('/spells?school=conjur')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        spells = Spell.query.where(Spell.school.like("%conjur%")).all()
        assert [s.id for s in spells] == [ s['id'] for s in res_data ]
        assert [s.name for s in spells] == [ s['name'] for s in res_data ]
        assert len(res_data) < len(Spell.query.all())

    def test_get_spell_by_id(self):
        """ <GET /spells/:id> retrieves a spell by id """

        db.session.add_all([
            Spell(**SPELL_ONE), 
            Spell(**SPELL_TWO), 
            Spell(**SPELL_THREE), 
            Spell(**SPELL_FOUR)
        ])
        db.session.commit()

        res = app.test_client().get('/spells/1')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        spell = Spell.query.first()
        assert res_data['id'] == spell.id 
        assert res_data['name'] == spell.name 

    def test_get_invalid_spell_by_id(self):
        """ <GET /spells/:id> returns a 404 error if no spell found """

        db.session.add_all([
            Spell(**SPELL_ONE), 
            Spell(**SPELL_TWO), 
            Spell(**SPELL_THREE), 
            Spell(**SPELL_FOUR)
        ])
        db.session.commit()

        res = app.test_client().get('/spells/6')
        assert res.status_code == 404
        assert res.content_type == 'application/json'
        res_data = res.json
        assert res_data['error']

    def test_post_spell(self):
        """ <POST /spells> creates and returns new spell """

        res = app.test_client().post( '/spells', json=SPELL_ONE )
        assert res.status_code == 201

        res_data = res.json
        assert res_data['id']
        assert res_data['name'] == SPELL_ONE['name']

        spell = Spell.query.where( Spell.name == SPELL_ONE['name'] ).first()
        assert spell

    def test_post_spell_returns_error_if_invalid(self):
        """ <POST /spells> creates and returns an error response if invalid """

        SPELL_DICT = {
            'name': 'Test Spell',
            'school': 'high school'
        }

        res = app.test_client().post( '/spells', json=SPELL_DICT )
        assert res.status_code == 422

        res_data = res.json
        assert res_data['error']

        spell = Spell.query.where( Spell.name == 'Test Spell' ).first()
        assert not spell

    def test_post_spell_ignores_unused_keys(self):
        """ <POST /spells> creates and returns a spell and ignores invalid keys """

        SPELL_DICT = {
            'name': 'Test Spell',
            'school': 'evocation',
            'thacko': 9001
        }

        res = app.test_client().post( '/spells', json=SPELL_DICT )
        assert res.status_code == 201

        res_data = res.json
        assert res_data['id']
        assert res_data['name'] == 'Test Spell'

        spell = Spell.query.where( Spell.name == 'Test Spell' ).first()
        assert spell

    def test_patch_spell(self):
        """ <PATCH /spells/:id> updates and returns an existing spell """

        SPELL_DICT = {
            'name': 'Test Spell',
            'school': 'evocation'
        }
        s = Spell(**SPELL_DICT)
        db.session.add(s)
        db.session.commit()

        res = app.test_client().patch( f"/spells/{s.id}", json={"name": "Updated Spell"} )
        assert res.status_code == 202

        res_data = res.json
        assert res_data['id'] == s.id
        assert res_data['name'] == 'Updated Spell'

    def test_patch_spell_returns_error_if_invalid(self):
        """ <PATCH /spells/:id> returns an error response if invalid """

        SPELL_DICT = {
            'name': 'Test Spell',
            'school': 'evocation'
        }
        s = Spell(**SPELL_DICT)
        db.session.add(s)
        db.session.commit()

        res = app.test_client().patch( f"/spells/{s.id}", json={"school": "mime arts"} )
        assert res.status_code == 422

        res_data = res.json
        assert res_data['error']

        spell = Spell.query.where( Spell.id == s.id ).first()
        assert spell.school != "mime arts"

    def test_patch_spell_ignores_unused_keys(self):
        """ <PATCH /spells> updates and returns a spell and ignores invalid keys """

        SPELL_DICT = {
            'name': 'Test Spell',
            'school': 'evocation'
        }
        s = Spell(**SPELL_DICT)
        db.session.add(s)
        db.session.commit()

        res = app.test_client().patch( f"/spells/{s.id}", json={ "name": "Super Spell", "thacko": "intense" } )
        assert res.status_code == 202

        res_data = res.json
        assert res_data['id']
        assert res_data['name'] == 'Super Spell'
        assert res_data.get('thacko') == None

        spell = Spell.query.where( Spell.id == s.id ).first()
        assert spell.name == 'Super Spell'
        
    
    def test_delete_spell_by_id(self):
        """ <DELETE /spells/:id> deletes a spell by id and returns a 204 No Content """

        db.session.add_all([
            Spell(**SPELL_ONE), 
            Spell(**SPELL_TWO), 
            Spell(**SPELL_THREE), 
            Spell(**SPELL_FOUR)
        ])
        db.session.commit()

        res = app.test_client().delete('/spells/1')
        assert res.status_code == 204

        spell = Spell.query.first()
        assert spell.id != 1

    def test_delete_invalid_spell_by_id(self):
        """ <DELETE /spells/:id> returns a 404 error if no spell found """

        db.session.add_all([
            Spell(**SPELL_ONE), 
            Spell(**SPELL_TWO), 
            Spell(**SPELL_THREE), 
            Spell(**SPELL_FOUR)
        ])
        db.session.commit()

        res = app.test_client().delete('/spells/6')
        assert res.status_code == 404
        assert res.content_type == 'application/json'
        res_data = res.json
        assert res_data['error']