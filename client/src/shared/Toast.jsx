// REACT //
import { useState, useEffect } from 'react'

// WRAPPER //
import ConditionalWrapper from 'shared/ConditionalWrapper'

function Toast({messages, toastType}) {

  // STATE //
  const [open, setOpen] = useState(true)

  // EFFECT //
  useEffect(() => {
    if (!open) {
      setOpen(true)
    }
  }, [messages])

  // COMPUTED ELEMENTS //
  const createMessages = () => (
    messages.constructor === Array
    ?
    messages.map(m => <span key={m}>{m}</span>)
    :
    (<span>{messages.message}</span>)
  )

  const openOrClosed = open ? "" : " closed"
  const className = "toast " + toastType

  // RENDER //
  return (
    <div
      className={"toast " + toastType + openOrClosed}
      onClick={open => setOpen(!open)}
    >
      <img src={toastImg} alt="" className="toast-frame" />
        {createMessages()}
    </div>
  )
}

export default ConditionalWrapper(Toast)

// TO USE:
//
// <Toast
//  displayCondition={showErrorsBoolean}
//  message={['You did something wrong and it made an error', 'Shame on you!']}
//  toastType='error'
// />
