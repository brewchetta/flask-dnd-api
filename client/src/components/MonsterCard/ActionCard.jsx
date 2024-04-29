function ActionCard({ action }) {

    const mappedActionParagraphs = action.description.split('\n').map((descP,i) => <p key={i}>{descP}</p>)

    return (
        <div className="">

            <h4>{action.name}</h4>
            
            { mappedActionParagraphs }

        </div>
    )

}

export default ActionCard