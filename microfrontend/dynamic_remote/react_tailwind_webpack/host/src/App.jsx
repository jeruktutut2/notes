import React, { lazy, Suspense, useEffect, useState } from "react";
import { BrowserRouter, Link, Route, Routes } from 'react-router-dom'
import { loadRemoteComponent } from "./loadRemoteComponent";

// export default function App() {
//   return <>
//     <div style={{ textAlign: "center", marginTop: "50px" }}>
//       <h1>Hello, React with Webpack!</h1>
//     </div>
//   </>
// };

const Remote = React.lazy(() => loadRemoteComponent(
    'http://localhost:3001/remoteEntry.js',
    'remote',
    './Remote'
  ).then((mod) => ({ default: mod.default || mod }))
);
const AboutRemote = React.lazy(() => loadRemoteComponent(
    'http://localhost:3001/remoteEntry.js',
    'remote',
    './AboutRemote'
  ).then((mod) => ({ default: mod.default || mod }))
);
const ProfileRemote = React.lazy(() => loadRemoteComponent(
    'http://localhost:3001/remoteEntry.js',
    'remote',
    './ProfileRemote'
  ).then((mod) => ({ default: mod.default || mod }))
);

const App = () => {
   // <div style={{ textAlign: "center", marginTop: "50px" }}>
   //  <h1>Hello, React with Webpack!</h1>
   // </div>
      // const [Remote, setRemote] = useState(null);
      // const [AboutRemote, setAboutRemote] = useState(null);
      // const [ProfileRemote, setProfileRemote] = useState(null);
      // const [error, setError] = useState(null);

      // useEffect(() => {
      //    loadRemoteComponent('http://localhost:3001/remoteEntry.js', 'remote', './Remote')
      //       .then(mod => setRemote(() => mod.default || mod));

      //    loadRemoteComponent('http://localhost:3001/remoteEntry.js', 'remote', './AboutRemote')
      //       .then(mod => setAboutRemote(() => mod.default || mod));

      //    loadRemoteComponent('http://localhost:3001/remoteEntry.js', 'remote', './ProfileRemote')
      //       .then(mod => setProfileRemote(() => mod.default || mod));
      // }, []);

      // if (!Remote || !AboutRemote || !ProfileRemote) return <div>Loading all components...</div>;

      return <>
            <div className="p-8 bg-gray-100 text-center">
               <h1 className="text-3xl font-bold text-blue-600">Hello Tailwind!</h1>
            </div>
            {/* <Suspense fallback={<div>Loading remote widget...</div>}>
               <Remote />
            </Suspense> */}
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
            {/* <Remote /> */}
            {/* <AboutRemote /> */}
            {/* <ProfileRemote /> */}
      </>
};

export default App;