from pathlib import Path


# create_nested_monster_routes_test #################################################
# model_name.lower():str = pluralized lowercase name
# model_name:class = model resources being tested
# model_test_data:dict = dictionary for creating test models
# model_invalid_data:dict = dictionary for raising expected errors
#       strings need double quotes with escapes as in "\"crocheting\""
# return None
# 
# creates and writes to a file to build a test for routes
# will not overwrite / regenerate files unless REGENERATE = True
# 
# keep REGENERATE = False to improve test suite speed
# ##########################################################################

REGENERATE = False

def create_nested_monster_models_test(model_name, model_test_data, model_invalid_data={}):

    test_file = Path(f'testing/models/model_{model_name.lower()}_test.py')
    if test_file.is_file() and not REGENERATE:
        print(f"File model_{model_name.lower()}_test.py already exists, manually delete it to regenerate or set REGENERATE=True")

    else:
        test_model_kargs_string = ", ".join( [ f"{k}=\"{model_test_data[k]}\"" for k in model_test_data.keys() ] )
        test_model_assert_attrs_string = "\n".join([ f"        assert db_item.{k} == s.{k}" for k in model_test_data.keys()])

        # VALIDATIONS # 
        validation_tests_strings = "\n".join( [ f"""\
    def test_validates_{k}(self):
        \""" (validations) Validates {model_name} {k} \"""
        db_item = {model_name}({test_model_kargs_string}, monster_id=1)
        db.session.add(db_item)
        db.session.commit()

        assert db_item.id

        with pytest.raises(ValueError):
            db_item.{k} = {model_invalid_data[k]}
            db.session.commit()

    """

        for k in model_invalid_data.keys()] )
        # END VALIDATIONS # 


        file_input = f"""\
import pytest

from create_app import create_app
from models import db, Monster, {model_name}
from testing.test_monsters import MONSTER_ONE

app = create_app('TESTING')

@pytest.fixture(autouse=True)
def run_before_and_after():
    with app.app_context():
        db.create_all()

        test_monster = Monster(**MONSTER_ONE)

        db.session.add(test_monster)
        db.session.commit()

        yield

        db.session.remove()
        db.drop_all()


class Test{model_name}:
    \""" [TESTING SUITE: <{model_name}>] \"""

    def test_{model_name}_has_attributes(self):
        \""" (attributes) Has proper attributes \"""
        s = {model_name}({test_model_kargs_string}, monster_id=1)
        db.session.add(s)
        db.session.commit()

        db_item = {model_name}.query.first()
        assert db_item
{test_model_assert_attrs_string}
        assert db_item.monster_id == 1

{validation_tests_strings}

    def test_belongs_to_monster(self):
        \""" (assocations) Belongs to a monster \"""
        s = {model_name}({test_model_kargs_string}, monster_id=1)
        db.session.add(s)
        db.session.commit()

        db_item = {model_name}.query.first()
        assert db_item
        assert db_item.monster
        assert db_item.monster.id == 1
"""

        f = open(f'testing/models/model_{model_name.lower()}_test.py', 'w')
        f.write(file_input)
        f.close()


# -----------TESTS BY MODEL----------- #


create_nested_monster_models_test("Skill", { "name": "history", "value": 2 }, { "name": "\"crocheting\"" } )

create_nested_monster_models_test("SpecialAbility", { "name": "Amphibious", "description": "Able to breathe air and water" } )

create_nested_monster_models_test("SavingThrow", { "name": "dex", "value": 2 }, { "name":"\"charm\"" } )

create_nested_monster_models_test("Sense", { "name": "darkvision", "distance": 60 } )

create_nested_monster_models_test("Speed", { "name": "walk", "distance": "60 ft." } )

create_nested_monster_models_test("Language", { "name": "sylvan" } )

create_nested_monster_models_test("Language", { "name": "sylvan" } )

create_nested_monster_models_test("DamageResistance", { "damage_type": "cold" }, { "damage_type": "\"fluffy\"" } )

create_nested_monster_models_test("DamageImmunity", { "damage_type": "fire" }, { "damage_type": "\"radioactive\"" } )

create_nested_monster_models_test("DamageVulnerability", { "damage_type": "thunder" }, { "damage_type": "\"supercalifragulisticexpeolodocious\"" } )

create_nested_monster_models_test("ConditionImmunity", { "condition_type": "poisoned" }, { "condition_type": "\"insane in the membrane\"" } )

create_nested_monster_models_test("Action", { "name": "Stabby Stab", "description": "Stabs with a dagger" } )