import React from 'react'
import ReactDOM from 'react-dom/client'
import routes from './routes'
import { createBrowserRouter, RouterProvider } from 'react-router-dom'
import './style/index.scss'

const router = createBrowserRouter(routes)

ReactDOM.createRoot(document.getElementById('root')).render(<RouterProvider router={router} />)