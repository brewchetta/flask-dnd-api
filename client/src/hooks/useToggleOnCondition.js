// REACT //
import { useState, useEffect } from 'react'

export default function useToggleOnCondition(condition) {

  // STATE //
  const [isOn, setIsOn] = useState(false)

  // EFFECT //
  useEffect(() => {
    if (!isOn && condition) {
      setIsOn(true)
    }
  }, [condition])

  // RETURN //
  return isOn
}

// when a condition is set to true, this will return true so long as the component is mounted
//
// TO USE:
//
// function App() {
//
// const [students, setStudents] = useState([])
// const [errors, setErrors] = useState([])
//
// const loaded = useToggleOnCondition(students.length)
//
// useEffect(() => {
//   fetch(...)
//   .then(...parse res)
//   .then(...setStudents)
//   .catch(...setErrors)
// }, [])
//
//   if (!loaded) return <div>Loading...</div>
//
//   return (<div>...components / errors</div>)
//
// }
