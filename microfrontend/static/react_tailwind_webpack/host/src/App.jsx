import React, { Suspense } from "react";

// export default function App() {
//   return <>
//     <div style={{ textAlign: "center", marginTop: "50px" }}>
//       <h1>Hello, React with Webpack!</h1>
//     </div>
//   </>
// };

const Remote = React.lazy(() => import('remote/Remote'));

const App = () => {
   // <div style={{ textAlign: "center", marginTop: "50px" }}>
   //  <h1>Hello, React with Webpack!</h1>
   // </div>
      return <>
            <div className="p-8 bg-gray-100 text-center">
               <h1 className="text-3xl font-bold text-blue-600">Hello Tailwind!</h1>
            </div>
            <Suspense fallback={<div>Loading remote widget...</div>}>
               <Remote />
            </Suspense>
      </>
};

export default App;