import React from "react"

const ButtonRemoteComponent = React.lazy(() => import("remote/Button"))
const TextRemoteComponent = React.lazy(() => import("remote/Text"))

function App() {
    return (
        <>
            <ButtonRemoteComponent />
            <TextRemoteComponent />
        </>
    )
}

export default App
