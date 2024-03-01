#!/usr/bin/env python3

from app import app
from models import db, Monster, Skill, SavingThrow, SpecialAbility, Sense, Language, DamageResistance, DamageImmunity, DamageVulnerability, ConditionImmunity, Action, Spell, MonsterSpell
from testing.test_monsters import MONSTER_ONE, MONSTER_TWO, MONSTER_THREE, MONSTER_FOUR, MONSTER_FIVE
from damage_types import DAMAGE_TYPES
from faker import Faker
import random

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

        print("\n Creating Senses")

        se1 = Sense(name='Devil Vision', monster=monsters[0])
        se2 = Sense(name='Darkvision', distance=120, monster=monsters[2])
        se3 = Sense(name='Blindsight', distance=30, monster=monsters[2])

        db.session.add_all([se1, se2, se3])
        db.session.commit()

        print(" Senses created...")

        print("\n Creating Languages")

        l1 = Language(name='infernal', monster=monsters[1])
        l2 = Language(name='common', monster=monsters[4])
        l3 = Language(name='sylvan', monster=monsters[4])

        db.session.add_all([l1, l2, l3])
        db.session.commit()

        print(" Languages created...")

        print("\n Creating DamageResistances")

        dr_list = []

        for _ in range(7):
            dr = DamageResistance(damage_type=random.choice(DAMAGE_TYPES), monster=random.choice(monsters))
            dr_list.append(dr)

        db.session.add_all(dr_list)
        db.session.commit()

        print(" DamageResistances created...")

        print("\n Creating DamageImmunities")

        dr_list = []

        for _ in range(3):
            dr = DamageImmunity(damage_type=random.choice(DAMAGE_TYPES), monster=random.choice(monsters))
            dr_list.append(dr)

        db.session.add_all(dr_list)
        db.session.commit()

        print(" DamageImmunities created...")

        print("\n Creating DamageVulnerabilities")

        dr_list = []

        for _ in range(3):
            dr = DamageVulnerability(damage_type=random.choice(DAMAGE_TYPES), monster=random.choice(monsters))
            dr_list.append(dr)

        db.session.add_all(dr_list)
        db.session.commit()

        print(" DamageVulnerabilities created...")

        print("\n Creating ConditionImmunities")

        ci_list = []

        for _ in range(5):
            ci = ConditionImmunity(condition_type=random.choice(ConditionImmunity.CONDITION_TYPES), monster=random.choice(monsters))
            ci_list.append(ci)

        db.session.add_all(ci_list)
        db.session.commit()

        print(" ConditionImmunities created...")

        print("\n Creating Actions")

        act_list = []

        for m in monsters:
            act = Action(
                    name="Dagger Dagger Dagger",
                    description="Throw three daggers",
                    monster=random.choice(monsters)
                )
            act_list.append(act)

        db.session.add_all(act_list)
        db.session.commit()

        print(" Actions created...")

        print("\n Creating Spells")

        sp1 = Spell(name="Burning Hands", description="2d6 fire damage and stuff", level=1, casting_time="action", duration="instant", range_area="15 foot cone", verbal=True, somatic=True, school="evocation", attack_save="dex", damage_type="fire")

        ms1 = MonsterSpell(spell=sp1, monster=monsters[0])

        sp2 = Spell(name="Cone of Cold", description="5d6 cold damage and stuff", level=1, casting_time="action", duration="instant", range_area="30 foot cone", verbal=True, somatic=True, school="evocation", attack_save="dex", damage_type="cold")

        ms2 = MonsterSpell(spell=sp2, monster=monsters[1])

        db.session.add_all([sp1, sp2, ms1, ms2])
        db.session.commit()

        print(" Spells created...")

        print("\nSeeding complete!")