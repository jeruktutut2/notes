import { useEffect } from "react"
export default function Callback() {
    
    useEffect(() => {
        const load = async () => {
            const params = new URLSearchParams(window.location.search)
            const code = params.get("code")
            console.log(code)
            const verifier = sessionStorage.getItem("pkce_verifier")
            console.log(verifier)

            const response = await fetch("http://localhost:8080/oauth/token", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: new URLSearchParams({
                    grant_type: "authorization_code",
                    code: code,
                    client_id: "client1",
                    // redirect_uri: "http://localhost:3000/callback",
                    code_verifier: verifier
                })
            })
            const data = await response.json()
            console.log(data)
        }
        load()
    }, [])

    return (
        <div>
            <h1>Callback</h1>
        </div>
    );
}