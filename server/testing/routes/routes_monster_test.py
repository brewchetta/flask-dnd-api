import pytest

from models import db, Monster
from create_app import create_app
from testing.test_monsters import MONSTER_ONE, MONSTER_TWO, MONSTER_THREE, MONSTER_FOUR, MONSTER_FIVE

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

class TestMonsterRoutes:
    """ [TESTING SUITE: <Monster routes>] """

    def test_get_monsters(self):
        """ <GET /monsters> retrieves a list of monsters """

        db.session.add_all([
            Monster(**MONSTER_ONE), 
            Monster(**MONSTER_TWO), 
            Monster(**MONSTER_THREE), 
            Monster(**MONSTER_FOUR), 
            Monster(**MONSTER_FIVE)
        ])
        db.session.commit()

        res = app.test_client().get('/monsters')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        monsters = Monster.query.all()
        assert [m.id for m in monsters] == [ m['id'] for m in res_data ]
        assert [m.name for m in monsters] == [ m['name'] for m in res_data ]

    def test_get_monsters_with_page(self):
        """ <GET /monsters?page=:int> retrieves a list of monsters offset by a page query defaulting at 10 monsters per page """

        mon_list = []
        for n in range(50):
            if n == 0:
                mon_list.append(Monster(**MONSTER_ONE))
            elif n == 10:
                mon_list.append(Monster(**MONSTER_TWO))
            elif n == 20:
                mon_list.append(Monster(**MONSTER_THREE))
            else:
                mon_list.append(Monster(**MONSTER_FIVE))

        db.session.add_all(mon_list)
        db.session.commit()

        res = app.test_client().get('/monsters?page=1')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert len(res_data) == 10
        assert res_data[0]['name'] == MONSTER_ONE['name']

        res = app.test_client().get('/monsters?page=2')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert len(res_data) == 10
        assert res_data[0]['name'] == MONSTER_TWO['name']

        res = app.test_client().get('/monsters?page=3')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert len(res_data) == 10
        assert res_data[0]['name'] == MONSTER_THREE['name']

    def test_get_monsters_with_page_count(self):
        """ <GET /monsters?page_count=:int> retrieves a list of monsters of a certain number on a page """

        mon_list = []
        for n in range(50):
            if n == 0:
                mon_list.append(Monster(**MONSTER_ONE))
            elif n == 4:
                mon_list.append(Monster(**MONSTER_TWO))
            elif n == 7:
                mon_list.append(Monster(**MONSTER_THREE))
            else:
                mon_list.append(Monster(**MONSTER_FIVE))

        db.session.add_all(mon_list)
        db.session.commit()

        res = app.test_client().get('/monsters?page_count=5')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert len(res_data) == 5
        assert res_data[0]['name'] == MONSTER_ONE['name']
        assert res_data[4]['name'] == MONSTER_TWO['name']

        res = app.test_client().get('/monsters?page_count=8')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert len(res_data) == 8
        assert res_data[0]['name'] == MONSTER_ONE['name']
        assert res_data[7]['name'] == MONSTER_THREE['name']

    def test_get_monsters_with_page_and_page_count(self):
        """ <GET /monsters?page_count=:int&page=:int> retrieves a list of monsters of a certain number offset by a number of pages """

        mon_list = []
        for n in range(50):
            if n == 5:
                mon_list.append(Monster(**MONSTER_TWO))
            elif n == 9:
                mon_list.append(Monster(**MONSTER_THREE))
            else:
                mon_list.append(Monster(**MONSTER_FIVE))

        db.session.add_all(mon_list)
        db.session.commit()

        res = app.test_client().get('/monsters?page_count=5&page=2')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        assert len(res_data) == 5
        assert res_data[0]['name'] == MONSTER_TWO['name']
        assert res_data[4]['name'] == MONSTER_THREE['name']

    def test_get_monsters_by_name(self):
        """ <GET /monsters> accepts a 'name' query that returns based on name """

        db.session.add_all([Monster(**MONSTER_ONE), Monster(**MONSTER_TWO), Monster(**MONSTER_THREE), Monster(**MONSTER_FOUR), Monster(**MONSTER_FIVE)])
        db.session.commit()

        res = app.test_client().get('/monsters?name=mon')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        monsters = Monster.query.where(Monster.name.like("%mon%")).all()
        assert [m.id for m in monsters] == [ m['id'] for m in res_data ]
        assert [m.name for m in monsters] == [ m['name'] for m in res_data ]
        assert len(res_data) < len(Monster.query.all())

    def test_get_monsters_by_category(self):
        """ <GET /monsters> accepts a 'category' query that returns based on category """

        db.session.add_all([
            Monster(**MONSTER_ONE), 
            Monster(**MONSTER_TWO), 
            Monster(**MONSTER_THREE), 
            Monster(**MONSTER_FOUR), 
            Monster(**MONSTER_FIVE)
        ])
        db.session.commit()

        res = app.test_client().get('/monsters?category=mon')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        monsters = Monster.query.where(Monster.category.like("%mon%")).all()
        assert [m.id for m in monsters] == [ m['id'] for m in res_data ]
        assert [m.name for m in monsters] == [ m['name'] for m in res_data ]
        assert len(res_data) < len(Monster.query.all())

    def test_get_monsters_by_sub_category(self):
        """ <GET /monsters> accepts a 'sub_category' query that returns based on sub_category """

        db.session.add_all([Monster(**MONSTER_ONE), Monster(**MONSTER_TWO), Monster(**MONSTER_THREE), Monster(**MONSTER_FOUR), Monster(**MONSTER_FIVE)])
        db.session.commit()

        res = app.test_client().get('/monsters?sub_category=born')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        monsters = Monster.query.where(Monster.sub_category.like("%born%")).all()
        assert [m.id for m in monsters] == [ m['id'] for m in res_data ]
        assert [m.name for m in monsters] == [ m['name'] for m in res_data ]
        assert len(res_data) < len(Monster.query.all())

    def test_get_monsters_by_size(self):
        """ <GET /monsters> accepts a 'size' query that returns based on size """

        db.session.add_all([Monster(**MONSTER_ONE), Monster(**MONSTER_TWO), Monster(**MONSTER_THREE), Monster(**MONSTER_FOUR), Monster(**MONSTER_FIVE)])
        db.session.commit()

        res = app.test_client().get('/monsters?size=medium')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        monsters = Monster.query.where(Monster.size.like("%medium%")).all()
        assert [m.id for m in monsters] == [ m['id'] for m in res_data ]
        assert [m.name for m in monsters] == [ m['name'] for m in res_data ]
        assert len(res_data) < len(Monster.query.all())

    def test_get_monster_by_id(self):
        """ <GET /monsters/:id> retrieves a monster by id """

        db.session.add_all([
            Monster(**MONSTER_ONE), 
            Monster(**MONSTER_TWO), 
            Monster(**MONSTER_THREE), 
            Monster(**MONSTER_FOUR), 
            Monster(**MONSTER_FIVE)
        ])
        db.session.commit()

        res = app.test_client().get('/monsters/1')
        assert res.status_code == 200
        assert res.content_type == 'application/json'
        res_data = res.json
        monster = Monster.query.first()
        assert res_data['id'] == monster.id 
        assert res_data['name'] == monster.name 

    def test_get_invalid_monster_by_id(self):
        """ <GET /monsters/:id> returns a 404 error if no monster found """

        db.session.add_all([
            Monster(**MONSTER_ONE), 
            Monster(**MONSTER_TWO), 
            Monster(**MONSTER_THREE), 
            Monster(**MONSTER_FOUR), 
            Monster(**MONSTER_FIVE)
        ])
        db.session.commit()

        res = app.test_client().get('/monsters/6')
        assert res.status_code == 404
        assert res.content_type == 'application/json'
        res_data = res.json
        assert res_data['error']

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

    def test_post_monster_returns_error_if_invalid(self):
        """ <POST /monsters> creates and returns an error response if invalid """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'lorge',
            'category': 'bitumenoid',
        }

        res = app.test_client().post( '/monsters', json=MONSTER_DICT )
        assert res.status_code == 422

        res_data = res.json
        assert res_data['error']

        monster = Monster.query.where( Monster.name == 'Test Monster' ).first()
        assert not monster

    def test_post_monster_ignores_unused_keys(self):
        """ <POST /monsters> creates and returns a monster and ignores invalid keys """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
            'thacko': True
        }

        res = app.test_client().post( '/monsters', json=MONSTER_DICT )
        assert res.status_code == 201

        res_data = res.json
        assert res_data['id']
        assert res_data['name'] == 'Test Monster'

        monster = Monster.query.where( Monster.name == 'Test Monster' ).first()
        assert monster

    def test_patch_monster(self):
        """ <PATCH /monsters/:id> updates and returns an existing monster """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }
        m = Monster(**MONSTER_DICT)
        db.session.add(m)
        db.session.commit()

        res = app.test_client().patch( f"/monsters/{m.id}", json={"name": "Monstar Test"} )
        assert res.status_code == 202

        res_data = res.json
        assert res_data['id'] == m.id
        assert res_data['name'] == 'Monstar Test'

    def test_patch_monster_returns_error_if_invalid(self):
        """ <PATCH /monsters/:id> returns an error response if invalid """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }
        m = Monster(**MONSTER_DICT)
        db.session.add(m)
        db.session.commit()

        res = app.test_client().patch( f"/monsters/{m.id}", json={"category": "mimic"} )
        assert res.status_code == 422

        res_data = res.json
        assert res_data['error']

        monster = Monster.query.where( Monster.id == m.id ).first()
        assert monster.category != "mimic"

    def test_patch_monster_ignores_unused_keys(self):
        """ <PATCH /monsters> updates and returns a monster and ignores invalid keys """

        MONSTER_DICT = {
            'name': 'Test Monster',
            'size': 'medium',
            'category': 'humanoid',
        }
        m = Monster(**MONSTER_DICT)
        db.session.add(m)
        db.session.commit()

        res = app.test_client().patch( f"/monsters/{m.id}", json={ "name": "Jimbo", "thacko": "wacko" } )
        assert res.status_code == 202

        res_data = res.json
        assert res_data['id']
        assert res_data['name'] == 'Jimbo'
        assert res_data.get('thacko') == None

        monster = Monster.query.where( Monster.id == m.id ).first()
        assert monster.name == 'Jimbo'
        
    
    def test_delete_monster_by_id(self):
        """ <DELETE /monsters/:id> deletes a monster by id and returns a 204 No Content """

        db.session.add_all([
            Monster(**MONSTER_ONE), 
            Monster(**MONSTER_TWO), 
            Monster(**MONSTER_THREE), 
            Monster(**MONSTER_FOUR), 
            Monster(**MONSTER_FIVE)
        ])
        db.session.commit()

        res = app.test_client().delete('/monsters/1')
        assert res.status_code == 204

        monster = Monster.query.first()
        assert monster.id != 1

    def test_delete_invalid_monster_by_id(self):
        """ <DELETE /monsters/:id> returns a 404 error if no monster found """

        db.session.add_all([
            Monster(**MONSTER_ONE), 
            Monster(**MONSTER_TWO), 
            Monster(**MONSTER_THREE), 
            Monster(**MONSTER_FOUR), 
            Monster(**MONSTER_FIVE)
        ])
        db.session.commit()

        res = app.test_client().delete('/monsters/6')
        assert res.status_code == 404
        assert res.content_type == 'application/json'
        res_data = res.json
        assert res_data['error']