# DnD Free Monster API

## Converting JSON Data

Place monster JSON files inside a `server/beyond_json_data/mosnters` and spells inside `server/beyond_json_data/spells`.

Example monster:

```json
{"index":"abjurer","name":"Abjurer","size":"Medium","type":"Humanoid","subtype":"Any Race","alignment":" Any Alignment","armor_class":12,"hit_points":84,"hit_dice":"13d8","speed":{"walk":"30 ft."},"strength":9,"dexterity":14,"constitution":14,"intelligence":18,"wisdom":12,"charisma":11,"spells":[{"name":"blade ward","level":0},{"name":"dancing lights","level":0},{"name":"mending","level":0},{"name":"message","level":0},{"name":"ray of frost","level":0},{"name":"alarm","level":1},{"name":"mage armor","level":1},{"name":"magic missile","level":1},{"name":"shield","level":1},{"name":"arcane lock","level":2},{"name":"invisibility","level":2},{"name":"counterspell","level":3},{"name":"dispel magic","level":3},{"name":"fireball","level":3},{"name":"banishment","level":4},{"name":"stoneskin","level":4},{"name":"cone of cold","level":5},{"name":"wall of force","level":5},{"name":"flesh to stone","level":6},{"name":"globe of invulnerability","level":6},{"name":"symbol","level":7},{"name":"teleport","level":7}],"spell_slots":{"1":4,"2":3,"3":3,"4":3,"5":2,"6":1,"7":1},"url":"https://www.dndbeyond.com/monsters","source":"Volo's Guide to Monsters","proficiencies":"Saving Throw: INT +8 | Saving Throw: WIS +5 | Skill: Arcana +8 | Skill: History +8","senses":"Passive Perception 11","languages":"any four languages","challenge_rating":"9","xp":5000,"spell_modifier":8,"spell_dc":16,"special_abilities":[{"name":"Spellcasting.","desc":" The abjurer is a 13th-level spellcaster. Its spellcasting ability is Intelligence (spell save DC 16, +8 to hit with spell attacks). The abjurer has the following wizard spells prepared:"},{"name":"Arcane Ward.","desc":" The abjurer has a magical ward that has 30 hit points. Whenever the abjurer takes damage, the ward takes the damage instead. If the ward is reduced to 0 hit points, the abjurer takes any remaining damage. When the abjurer casts an abjuration spell of 1st level or higher, the ward regains a number of hit points equal to twice the level of the spell."}],"actions":[{"name":"QuarterstaffMelee Weapon Attack:","desc":" +3 to hit, reach 5 ft., one target. Hit: 2 (1d6 − 1) bludgeoning damage, or 3 (1d8 − 1) bludgeoning damage if used with two hands."}]}
```

Example spell:

```json
{"index":"acid-splash","name":"Acid Splash","description":"You hurl a bubble of acid. Choose one or two creatures you can see within range. If you choose two, they must be within 5 feet of each other. A target must succeed on a Dexterity saving throw or take 1d6 acid damage.\nThis spell’s damage increases by 1d6 when you reach 5th level (2d6), 11th level (3d6), and 17th level (4d6).\n","level":0,"casting_time":"1 Action","ritual":false,"duration":"Instantaneous","concentration":false,"range_area":"60 ft","verbal":true,"somatic":true,"school":"Conjuration","attack_save":"DEX Save","damage_effect":"Acid","source":"Basic Rules, pg. 211","url":"https://www.dndbeyond.com/spells/acid-splash"}
```

In order to add the data to the database:

```bash
cd server
python convert_json_data.py
```

Inside `convert_json_data.py` there are two constants that can be changed:

```python
DEBUG = True
# toggle to turn on verbose debug text in the terminal

LOG = True
# toggle to write errors into the log.txt file in beyond_json_data folder
```

Conversion will first remove all data before seeding the database. Will attempt to seed spells first followed by monsters and create relational data between spells and monsters if able.