import React, { lazy, Suspense } from "react";
import Remote from "./components/Remote";
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import AboutRemote from "./components/AboutRemote";
import ProfileRemote from "./components/ProfileRemote";

// export default function App() {
//   return <>
//     <div style={{ textAlign: "center", marginTop: "50px" }}>
//       <h1>Hello, React with Webpack!</h1>
//     </div>
//   </>
// };

const App = () => {
   // <div style={{ textAlign: "center", marginTop: "50px" }}>
   //  <h1>Hello, React with Webpack!</h1>
   // </div>
   return <>
      <div className="p-8 bg-gray-100 text-center">
         <h1 className="text-3xl font-bold text-blue-600">Hello Remote</h1>
      </div>
      <BrowserRouter>
         <nav>
            <Link to="/">App</Link> | <Link to="/about">About</Link> | <Link to="/profile">Profil</Link>
         </nav>
         <Routes>
            <Route path='/' element={<Suspense fallback="Loading..."><Remote /></Suspense>}/>
            <Route path='/about' element={<Suspense fallback="Loading..."><AboutRemote /></Suspense>}/>
            <Route path='/profile' element={<Suspense fallback="Loading..."><ProfileRemote /></Suspense>}/>
         </Routes>
      </BrowserRouter>
   </>
};

export default App;