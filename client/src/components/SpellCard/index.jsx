function SpellCard({ spell }) {

    const mappedDescriptionParagraphs = spell.description
    .split('\n')
    .map((d,i) => <p key={i}>{d}</p>)

    return (
        <div className="border-black padding-small">


            <h4>{spell.name}</h4>
            <p>{spell.source} | Level {spell.level}</p>

            <p>Attack/Save {spell.attack_save} | Damage/Effect {spell.damage_effect}</p>

                { mappedDescriptionParagraphs }

            <p>Casting Time {spell.casting_time} | Duration {spell.duration} | Range/Area {spell.range_area}</p>
            <p>Concentration - {spell.concentration ? 'Yes' : 'No'} | Ritual - {spell.ritual ? 'Yes' : 'No'}</p>

            <p>Components: {spell.verbal && 'verbal'} {spell.somatic && 'somatic'} {spell.material && `material (${spell.material})`}</p>

        </div>
    )

}

export default SpellCard