from models import Monster
from app import app, db

class TestRoutes:
    """ [TESTING SUITE: <routes>] """

    def test_get_monsters(self):
        """ <GET /monsters> retrieves a list of monsters """

        with app.app_context():
            m1 = Monster()
            m2 = Monster()
            db.session.add_all([m1, m2])
            db.session.commit()

            res = app.test_client().get('/monsters')
            assert res.status_code == 200
            assert res.content_type == 'application/json'
            res_data = res.json
            monsters = Monster.query.all()
            assert [m['id'] for m in monsters] == [ m['id'] for m in res_data ]
            assert [m['name'] for m in monsters] == [ m['name'] for m in res_data ]

    def test_post_monster(self):
        """ <POST /monsters> creates and returns new monster """

        with app.app_context():
            # TODO: Insert other attributes here (use a dict)
            MONSTER_DICT = {
                'name': 'Test Monster'
            }

            res = app.test_client().post( '/monsters', json=MONSTER_DICT )
            assert res.status_code == 201

            res_data = res.json
            assert res_data['id']
            assert res_data['name'] == 'Test Monster'

            monster = Monster.query.where( Monster.name == 'Test Monster' ).first()
            assert monster