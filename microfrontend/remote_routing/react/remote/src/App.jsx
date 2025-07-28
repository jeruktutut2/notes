import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import './App.css'
import AppView from "./views/AppView"
import AboutView from "./views/AboutView"
import ProfileView from "./views/ProfileView"
import { Suspense } from 'react'

function App() {
    return (
        <>
            <BrowserRouter>
                <nav>
                    <Link to="/">App</Link>
                    <Link to="/about">About</Link>
                    <Link to="/profile">Profile</Link>
                </nav>
                <Routes>
                    <Route path='/' element={<Suspense fallback="Loading..."><AppView /></Suspense>} />
                    <Route path='/about' element={<Suspense fallback="Loading..."><AboutView /></Suspense>} />
                    <Route path='/profile' element={<Suspense fallback="Loading..."><ProfileView /></Suspense>} />
                </Routes>
            </BrowserRouter>
        </>
    )
}

export default App
