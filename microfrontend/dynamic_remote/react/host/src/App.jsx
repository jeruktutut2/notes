import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import { useState, useEffect } from 'react'
// import reactLogo from './assets/react.svg'
// import viteLogo from '/vite.svg'
import './App.css'
import { lazy, Suspense } from 'react'
import { loadRemote } from './loadRemote'

const ButtonRemoteComponent = lazy(() => loadRemote('remote', 'http://localhost:3001', './Button'))
// const TextRemoteComponent = lazy(() => loadRemote('remote', 'http://localhost:3001', './Text'))
// const AppRemoteView = lazy(() => loadRemote('remote', 'http://localhost:3001', './AppView'))
// const AboutRemoteView = lazy(() => loadRemote('remote', 'http://localhost:3001', './AboutView'))
// const ProfileRemoteView = lazy(() => loadRemote('remote', 'http://localhost:3001', './ProfileView'))

function App() {
  // const [count, setCount] = useState(0)
    const [ButtonRemoteComponent, setButtonRemoteComponent] = useState(null);

    useEffect(() => {
        loadRemote('remote', 'http://localhost:3001', './Button')
        .then((module) => {
          setButtonRemoteComponent(() => module);
        })
        .catch((err) => {
            console.error('Gagal memuat modul remote:', err);
        });
    }, []);

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
            <ButtonRemoteComponent />
            {/* <TextRemoteComponent /> */}
            {/* <BrowserRouter>
                <nav>
                    <Link to="/">App</Link>
                    <Link to="/about">About</Link>
                    <Link to="/profile">Profile</Link>
                </nav>
                <Routes>
                    <Route path='/' element={<Suspense fallback="Loading..."><AppRemoteView /></Suspense>} />
                    <Route path='/about' element={<Suspense fallback="Loading..."><AboutRemoteView /></Suspense>} />
                    <Route path='/profile' element={<Suspense fallback="Loading..."><ProfileRemoteView /></Suspense>} />
                </Routes>
            </BrowserRouter> */}
        </>
    )
}

export default App
