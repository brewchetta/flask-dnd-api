#!/usr/bin/env python3

from app import app
from models import db, Monster, Skill, SavingThrow, SpecialAbility
from testing.test_monsters import MONSTER_ONE, MONSTER_TWO, MONSTER_THREE, MONSTER_FOUR, MONSTER_FIVE
from faker import Faker

faker = Faker()

if __name__ == '__main__':
    with app.app_context():

        print("Seeding database...")

        db.create_all()

        print("\n Deleting old data...")

        Monster.query.delete()
        Skill.query.delete()
        SavingThrow.query.delete()

        print("\n Adding monster data...")

        for m_dict in [MONSTER_ONE, MONSTER_TWO, MONSTER_THREE, MONSTER_FOUR, MONSTER_FIVE]:
            m = Monster(**m_dict)
            db.session.add(m)
            db.session.commit()
            print(f"  Created {m.name}...")

        print("\n Creating Skills")

        monsters = Monster.query.all()
            
        s1 = Skill(name='history', value=1, monster=monsters[0])
        s2 = Skill(name='arcana', value=2, monster=monsters[0])
        s3 = Skill(name='perception', value=3, monster=monsters[1])
        s4 = Skill(name='animal handling', value=4, monster=monsters[1])
        s5 = Skill(name='athletics', value=5, monster=monsters[2])

        db.session.add_all([s1, s2, s3, s4, s5])
        db.session.commit()

        print(" Skills created...")
        
        print("\n Creating SavingThrows")

        st1 = SavingThrow(name='intelligence', value=1, monster=monsters[0])
        st2 = SavingThrow(name='dexterity', value=2, monster=monsters[0])
        st3 = SavingThrow(name='strength', value=3, monster=monsters[1])
        st4 = SavingThrow(name='charisma', value=4, monster=monsters[1])
        st5 = SavingThrow(name='constitution', value=5, monster=monsters[2])

        db.session.add_all([st1, st2, st3, st4, st5])
        db.session.commit()

        print(" SavingThrows created...")

        print("\n Creating SpecialAbilities")

        sa1 = SpecialAbility(name='Water Walk', description="Able to walk on water", monster=monsters[0])
        sa2 = SpecialAbility(name='Amphibious', description="Able to breathe air and water", monster=monsters[1])
        sa3 = SpecialAbility(name='Hungry', description="So hungry", monster=monsters[2])
        sa4 = SpecialAbility(name='Turn Undead Resistant', description="Something about turning undead", monster=monsters[3])
        sa5 = SpecialAbility(name='Blabbermouth', description="Getting in range of this monster will make you made", monster=monsters[4])

        db.session.add_all([sa1, sa2, sa3, sa4, sa5])
        db.session.commit()

        print(" SpecialAbilities created...")

        print("\nSeeding complete!")