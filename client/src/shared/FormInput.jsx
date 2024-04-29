// REACT //
import { useRef } from 'react'

function FormInput({name, inputType="text", labelText, onChange, value}) {

  // REF //
  const input = useRef()

  // EVENT CALLBACK //
  function handleClickLabel() {
    input.current.focus()
  }

  // RENDER //
  return (
    <>

      {
        labelText
        ?
        <label htmlFor={name} onClick={handleClickLabel}>{labelText}</label>
        :
        null
      }

      <input
        ref={input}
        type={inputType}
        name={name}
        onChange={onChange}
        value={value}
      />

    </>
  )

}

export default FormInput

// TO USE:
//
// <FormInput
//  name="password"
//  inputType="password"
//  labelText="Password"
//  onChange={handleChange}
//  value={username}
//  className="some-great-css-class"
// />
//
