import ActionCard from './ActionCard'
import AbilityCard from './AbilityCard'
import IteratedItemsCard from './IteratedItemsCard'
import SpellCard from '../SpellCard'

function MonsterCard({ monster }) {

    const mappedActions = monster.actions
    .filter(a => !a.reaction && !a.bonus_action && !a.legendary_action && !a.lair_action)
    .map(a => <ActionCard key={a.id} action={a} />)

    const mappedReactions = monster.actions
    .filter(a => a.reaction)
    .map(a => <ActionCard key={a.id} action={a} />)

    const mappedBonusActions = monster.actions
    .filter(a => a.bonus_action)
    .map(a => <ActionCard key={a.id} action={a} />)

    const mappedLegendaryActions = monster.actions
    .filter(a => a.legendary_action)
    .map(a => <ActionCard key={a.id} action={a} />)
    
    const mappedLairActions = monster.actions
    .filter(a => a.lair_action)
    .map(a => <ActionCard key={a.id} action={a} />)

    const mappedAbilities = monster.special_abilities.map(a => <AbilityCard key={a.id} ability={a} />)

    const hitDiceString = `(${monster.hit_dice_count}d${monster.hit_dice_size}${
        monster.constitution !== 10 && monster.constitution !== 11 ? ` + ${Math.floor((monster.constitution - 10) / 2) * monster.hit_dice_count}` : ''
    })`

    return (
        <div className="border-black padding-medium">

            <h2>{monster.name}</h2>
            <p>{monster.source} | Challenge Rating: {monster.challenge_rating}</p>
            <p>{monster.alignment} {monster.size} {monster.category} {monster.sub_category ? `(${monster.sub_category})` : null}</p>
            <p>{monster.hit_points} hitpoints {hitDiceString} | {monster.armor_class} AC</p>
            <p>{monster.strength} STR | {monster.dexterity} DEX | {monster.constitution} CON</p>
            <p>{monster.intelligence} INT | {monster.wisdom} WIS | {monster.charisma} CHA</p>

            <IteratedItemsCard title='Saving Throws' items={monster.saving_throws.map(s => `${s.name} ${s.value > 0 ? `+${s.value}` : s.value}`)} />

            <IteratedItemsCard title='Senses' items={monster.senses.map(s => `${s.name} ${s.distance}ft.`)} />

            <p>Passive Perception {monster.passive_perception}</p>

            <IteratedItemsCard title='Skills' items={monster.skills.map(s => `${s.name} ${s.value > 0 ? '+' + s.value : s.value}`)} />

            <p>Speed: { monster.speeds.map(s => `${s.name} ${s.distance}`).join(' | ') }</p>

            <IteratedItemsCard title={'Condition Immunities'} items={monster.condition_immunities.map(item => item.condition_type)} />

            <IteratedItemsCard title={'Damage Immunities'} items={monster.damage_immunities.map(item => item.damage_type)} />

            <IteratedItemsCard title={'Damage Resistances'} items={monster.damage_resistances.map(item => item.damage_type)} />

            <IteratedItemsCard title={'Damage Vulnerabilities'} items={monster.damage_vulnerabilities.map(item => item.damage_type)} />

            <IteratedItemsCard title={'Langauges'} items={monster.languages.map(item => item.name)} />

            { mappedAbilities.length ? <h3>Special Abilities</h3> : null }

            { mappedAbilities }

            { mappedActions.length ? <h3>Actions</h3> : null }

            { mappedActions }

            { mappedBonusActions.length ? <h3>Bonus Actions</h3> : null }

            { mappedBonusActions }

            { mappedLegendaryActions.length ? <h3>Legendary Actions</h3> : null }

            { mappedLegendaryActions }

            { mappedLairActions.length ? <h3>Lair Actions</h3> : null }

            { mappedLairActions }

            { 
                monster.spells.length
                ?
                <>
                    <h3>Spells</h3>
                    { monster.spells.map(s => <SpellCard key={s.id} spell={s} />) }
                </>
                :
                null
            }

        </div>
    )

}

export default MonsterCard