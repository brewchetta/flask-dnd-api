// REACT //
import { useRef } from 'react'

function FormCheckbox({name, labelText, onChange, value, checked, disabled, className}) {

  // REF //
  const input = useRef()

  // EVENT CALLBACK //
  function handleClickLabel() {
    input.current.click()
  }

  // RENDER //
  return (
    <div className={className}>

      <input
        ref={input}
        type="checkbox"
        name={name}
        onChange={onChange}
        checked={value || checked}
        disabled={disabled}
        className={className || 'boxmark'}
      />

      {
        labelText
        ?
        <label htmlFor={name} onClick={handleClickLabel}>{labelText}</label>
        :
        null
      }

    </div>
  )

}

export default FormCheckbox

// TO USE:
//
// <FormCheckbox
//  name="dark-mode"
//  labelText="Dark Mode"
//  onChange={handleClick}
//  checked={isDarkMode}
//  className="some-great-css-class"
// />
//
