import MainOutlet from './components/MainOutlet'
import Home from './components/Home'

const routes = [

    // MAIN OUTLET
    {
        element: <MainOutlet />,
        path: '/',
        children: [
            {
                index: true,
                element: <Home />
            }
        ]
    }

]

export default routes