import React from "react";
import Remote from "./components/Remote";

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
      <Remote />
   </>
};

export default App;