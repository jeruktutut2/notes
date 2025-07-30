import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { BrowserRouter, Route, Routes } from 'react-router'
import ComponentA from "./components/ComponentA.jsx"
import ComponentB from "./components/ComponentB.jsx"
import ComponentC from "./components/ComponentC.jsx"

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        {/* <App /> */}
        <Route path="/" element={<App />}/>
        <Route path="/component-a" element={<ComponentA />}/>
        <Route path="/component-b" element={<ComponentB />} />
        <Route path="/component-c" element={<ComponentC />}/>
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
