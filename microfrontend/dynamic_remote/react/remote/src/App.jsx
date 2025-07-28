import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
// import { useState } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
import { Suspense } from 'react'
import AppView from "./views/AppView"
import AboutView from "./views/AboutView"
import ProfileView from "./views/ProfileView"
import Button from "./components/Button"
import Text from "./components/Text"

function App() {
  // const [count, setCount] = useState(0)

    return (
        <>
      {/* <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div> */}
      {/* <h1>Vite + React</h1> */}
      {/* <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div> */}
      {/* <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p> */}
            <Button />
            <Text />
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
