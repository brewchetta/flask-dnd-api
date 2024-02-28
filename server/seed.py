#!/usr/bin/env python3

from app import app
from models import db, Monster, Skill
from testing.test_monsters import MONSTER_ONE, MONSTER_TWO, MONSTER_THREE, MONSTER_FOUR, MONSTER_FIVE
from faker import Faker

faker = Faker()

if __name__ == '__main__':
    with app.app_context():

        print("Seeding database...")

        db.create_all()

        print(" Deleting old data...")

        Monster.query.delete()
        Skill.query.delete()

        print(" Adding monster data...")

        for m_dict in [MONSTER_ONE, MONSTER_TWO, MONSTER_THREE, MONSTER_FOUR, MONSTER_FIVE]:
            m = Monster(**m_dict)
            db.session.add(m)
            db.session.commit()
            print(f"  Created {m.name}...")

        print(" Creating Skills")

        monsters = Monster.query.all()
            
        s1 = Skill(name='history', value=1, monster=monsters[0])
        s2 = Skill(name='arcana', value=2, monster=monsters[0])
        s3 = Skill(name='perception', value=3, monster=monsters[1])
        s4 = Skill(name='animal handling', value=4, monster=monsters[1])
        s5 = Skill(name='athletics', value=5, monster=monsters[2])

        db.session.add_all([s1, s2, s3, s4, s5])
        db.session.commit()

        print(" Skills created...")

        print("Seeding complete!")