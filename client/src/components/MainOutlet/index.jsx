import { Outlet } from 'react-router-dom'

function MainOutlet() {
  return (
    <>
      <div className="app">

        {/* navbar would go here */}

        <Outlet />

      </div>
    </>
  )
}

export default MainOutlet