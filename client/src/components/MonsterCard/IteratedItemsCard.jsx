function IteratedItemsCard({title, items, joinDivider=', '}) {

    if (items.length) {
        const joinedItems = items.join(joinDivider)
    
        return (
            <div>
                
                <h3>{title}</h3>
                
                { joinedItems }
            
            </div>
        )

    } else {
        return null
    }

}

export default IteratedItemsCard