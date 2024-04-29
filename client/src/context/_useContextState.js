import { useState, useContext, createContext } from 'react'
import { capitalize } from 'utils/string'

function CreateStatefulContextWrapper(defaultState, stateName='state', callback) {
  const StatefulContext = createContext()

  function StatefulContextWrapper( { children } ) {
    const [state, setState] = useState(defaultState)

    function applyState( newState ) {

      // applies a callback when setting state if present
      if (callback && typeof newState === 'function') {
        setState( prev  => callback( newState( prev ) ) )

      // applies state as a function if present and no callback
      } else if (callback) {
        setState( callback( newState ) )

      // applies state if not a function
      } else {
        setState(newState)
      }

    }

    return (
      <StatefulContext.Provider value={ { [stateName]: state, [`set${capitalize(stateName)}`]: applyState } }>
        {children}
      </StatefulContext.Provider>
    )
  }

  const useStatefulContext = () => useContext(StatefulContext)

  return [useStatefulContext, StatefulContextWrapper]
}

export default CreateStatefulContextWrapper
