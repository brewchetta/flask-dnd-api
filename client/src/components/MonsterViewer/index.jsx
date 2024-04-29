import { useState } from 'react'
import MonsterCard from '../MonsterCard'

function MonsterViewer() {

    const [monsterSearchInput, setMonsterSearchInput] = useState('')
    const [searchResults, setSearchResults] = useState([])

    console.log(searchResults)

    const handleSubmit = async e => {
        e.preventDefault()
        const res = await fetch(`http://localhost:5000/monsters?name=${monsterSearchInput}`)
        if (res.ok) {
            const data = await res.json()
            setSearchResults(data)
        }
    }

    const mappedMonsters = searchResults.map(m => <MonsterCard key={m.id} monster={m} />)

    return (
        <div>
            <h2>Look Up A Monster</h2>

            <form onSubmit={handleSubmit}>

                <input type="text"
                onChange={ e => setMonsterSearchInput(e.target.value) }
                value={monsterSearchInput} />

                <input type="submit" value="Search by Name" />

                { mappedMonsters }

            </form>
        </div>
    )

}

export default MonsterViewer