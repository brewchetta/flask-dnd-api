function FormSelect({name, labelText, onChange, value, children, defaultText}) {

    const defaultOption = defaultText && value === 'default' ? <option value={'default'}>{defaultText}</option> : null
  
    // RENDER //
    return (
      <>
  
        {labelText ? <label htmlFor={name}>{labelText}</label> : null}
  
        <select
          name={name}
          onChange={onChange}
          value={value}
        >
  
          {defaultOption}
  
          {children}
  
        </select>
  
      </>
    )
  
  }
  
  export default FormSelect
  
  // TO USE:
  //
  // <FormSelect
  //  name='country'
  //  labelText='Choose Your Country'
  //  onChange={handleChange}
  //  value={currentCountry}
  //  defaultText='none'
  // >
  //
  //    <option value='guatemala'>Guatemala</option>
  //    <option value='colombia'>Colombia</option>
  //    <option value='mexico'>Mexico</option>
  //
  // </FormSelect>
  //
  // The default text will create a default option with a value of 'default' if used or otherwise none if not
  