import { lazy, Suspense } from 'react'
import './App.css'
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'

const AppRemoteView = lazy(() => import("remote/AppView"))
const AboutRemoteView = lazy(() => import("remote/AboutView"))
const ProfileRemoteView = lazy(() => import("remote/ProfileView"))

function App() {
    return (
        <>
            <BrowserRouter>
                <nav>
                    <Link to="/">App</Link> | <Link to="/about">About</Link> | <Link to="/profile">Profil</Link>
                </nav>
                <Routes>
                    {/* <Route path="/" element={<h1>Home Page</h1>} /> */}
                    <Route path='/' element={<Suspense fallback="Loading..."><AppRemoteView /></Suspense>}/>
                    <Route path='/about' element={<Suspense fallback="Loading..."><AboutRemoteView /></Suspense>}/>
                    <Route path='/profile' element={<Suspense fallback="Loading..."><ProfileRemoteView /></Suspense>}/>
                </Routes>
            </BrowserRouter>
        </>
    )
}

export default App
