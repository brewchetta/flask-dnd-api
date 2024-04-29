function AbilityCard({ ability }) {

    const mappedAbilityParagraph = ability.description.split('\n').map((descP, i) => <p key={i}>{descP}</p>)

    return (
        <div className="">

            <h4>{ability.name}</h4>

            {mappedAbilityParagraph}

        </div>
    )

}

export default AbilityCard