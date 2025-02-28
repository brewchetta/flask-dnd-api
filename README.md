# D&D Monster API

This is a RESTful Flask API that can be populated with Dungeons & Dragons monsters and spells. This application does not come with an associated database or monster/spell data, it will be up to the user to populate data based on official D&D content, rulebooks, or their own custom content.

## Contents

- [Local Installation](#local-installation)
    - [ENV](#env)
    - [With Pipenv](#with-pipenv)
    - [With Pip](#with-pip)
- [Usage](#usage)
    - [Endpoints](#endpoints)
- [Converting JSON Data](#converting-json-data)
    - [Limitations](#limitations)
    - [JSON Examples](#json-examples)
- [Contributing](#contributing)

## Local Installation 

### ENV

You will need the following variables to use this application:

```
FLASK_ENV=PRODUCTION/DEVELOPMENT/TEST
DATABASE_URI=your-postgresql-db-here
```

By default the `FLASK_ENV` will be set to `DEVELOPMENT` and the `DATABASE_URI` will only get used in `PRODUCTION` mode.

The `DEVELOPMENT` database defaults to a local `sqlite` database.

### With Pipenv

The local server uses pipenv to create a virtual environment. This is preferred in order to not clutter the global space.

```
pipenv install
pipenv shell

cd server
flask db upgrade
flask run
```

## With Pip

You may also install files globally using pip.

```
pip install SQLAlchemy, flask, flask-sqlalchemy, flask-migrate, pytest, importlib-metadata, importlib-resources, sqlalchemy-serializer, flask-cors, psycopg2-binary

cd server
flask db upgrade
flask run
```

## Usage

You can start the server with `flask run`. By default the application is served on `127.0.0.1:5000`.

### Endpoints

The majority of endpoints can be accessed with `GET`, `POST`, `PATCH`, and `DELETE` methods.

```
/monsters
/monsters/:id
/monsters/:id/spells
/monsters/:id/skills
/monsters/:id/saving_throws
/monsters/:id/special_abilities
/monsters/:id/senses
/monsters/:id/speeds
/monsters/:id/languages
/monsters/:id/damage_resistances
/monsters/:id/damage_immunities
/monsters/:id/damage_vulnerabilities
/monsters/:id/condition_immunities
/monsters/:id/actions
/spells
```

## Converting JSON Data

Place monster JSON files inside a `server/beyond_json_data/monsters` and spells inside `server/beyond_json_data/spells`.

An example of the file structure:

```
├── server
|   ├── beyond_json_data
|   │   ├── monsters
|   │   │   └── abjurer.json
|   │   └── spells
|   │       └── acid-splash.json
```

In order to add the data to the database you may use the `convert_json_data` script:

```bash
cd server
python convert_json_data.py
```

Inside `convert_json_data.py` there are two variables that can be changed for improved usability:

```python
DEBUG = True
# toggle to turn on verbose debug text in the terminal

LOG = True
# toggle to write errors into the log.txt file in beyond_json_data folder
```

Conversion will first remove all data before adding to the database. The script will attempt to seed spells first followed by monsters and create relational data between spells and monsters if able.

### JSON Examples

You may find an example monster in [abjurer.json](examples/abjurer.json) and an example spell in [acid-splash.json](examples/acid-splash.json).

### Limitations

The conversion script currently does not account for bonus actions and reactions. This will be fixed in an update.

## Contributing

Check out our `CONTRIBUTING.md`. For issues please remember to be kind and follow what you'd expect from general community guidelines.