'use client'
import { useEffect, useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
// import * as SystemJS from 'systemjs'

function App() {
  const [count, setCount] = useState(0)
  const [ComponentA, setComponentA] = useState(null)
  const [ComponentB, setComponentB] = useState(null)
  const [ComponentC, setComponentC] = useState(null)

  useEffect(() => {
    console.log(1)
    const loadComponent = async() => {
      console.log(2)
      try {
        console.log(3)
        // const mod = await SystemJS.import('http://localhost:4173/react-remote.umd.js');
        const mod = await System.import('http://localhost:4173/react-remote.umd.js');
        // const mod = await System.import('http://localhost:4173/vue-remote.umd.js');
        console.log(4)
        setComponentA(() => mod.ComponentA)
        console.log(5, ComponentA)
        setComponentB(() => mod.ComponentB)
        console.log(6, ComponentB)
        setComponentC(() => mod.ComponentC)
        console.log(7, ComponentC)
      } catch(e) {
        console.log(8)
        console.log("e:", e)
      }
    }
    loadComponent()
    console.log(9)
  }, [])

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>

      <h1>Component</h1>
      {ComponentA != undefined && ComponentA != null ? console.log("ComponentA:", ComponentA) : <p>Loading...</p>}
      {ComponentA != undefined && ComponentA != null ? <ComponentA /> : <p>Loading...</p>}
      {/* {ComponentB ? <ComponentB /> : <p>Loading...</p>} */}
      {/* {ComponentC ? <ComponentC /> : <p>Loading...</p>} */}

    </>
  )
}

export default App
