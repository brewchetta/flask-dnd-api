#!/usr/bin/env python3

from app import app
from models import db, Monster
from testing.test_monsters import MONSTER_ONE, MONSTER_TWO, MONSTER_THREE, MONSTER_FOUR, MONSTER_FIVE
from faker import Faker

faker = Faker()

if __name__ == '__main__':
    with app.app_context():

        print("Seeding database...")

        db.create_all()

        print(" Deleting old data...")

        Monster.query.delete()

        print(" Adding monster data...")

        for m_dict in [MONSTER_ONE, MONSTER_TWO, MONSTER_THREE, MONSTER_FOUR, MONSTER_FIVE]:
            m = Monster(**m_dict)
            db.session.add(m)
            db.session.commit()
            print(f"  Created {m.name}...")

        print("Seeding complete!")