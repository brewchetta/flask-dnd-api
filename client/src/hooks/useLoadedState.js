// REACT //
import { useState, useEffect } from 'react'

export default function useLoadedState(defaultState, url) {

  // STATE //
  const [state, setState] = useState(defaultState)
  const [errors, setErrors] = useState([])
  const [loading, setLoading] = useState(true)

  // EFFECT //
  useEffect( async () => {
    const res = await fetch(url)
    if (res.ok) {
        const data = await res.json()
        setState(data)
    } else {
        // structure errors you'll need here!
        setErrors( ['Error: Something went wrong'] )
    }
  }, [])

  // RETURN //
  return [state, setState, errors, setErrors, loading]
}
