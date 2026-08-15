import { Routes, Route } from "react-router-dom"
import Home from "./pages/Home"
import Login from "./pages/Login"
import Callback from "./pages/Callback"

export default function App() {
    return (
        // <div>
        //   <h1>React SPA with Webpack</h1>
        // </div>

        <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/callback" element={<Callback />} />
        </Routes>
    );
}
