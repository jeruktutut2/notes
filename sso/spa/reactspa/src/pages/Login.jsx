import { useEffect } from "react"

export default function Login() {
    useEffect(() => {
        // TODO: Implement PKCE flow
        const load = async () => {
            const { verifier, challenge } = await createPKCE()
            // console.log(verifier, challenge)
            sessionStorage.setItem("pkce_verifier", verifier)
            // const redirect = encodeURIComponent("http://localhost:3000/callback")
            // const authUrl = `http://localhost:8080/oauth/authorize?response_type=code&client_id=reactspa&redirect_uri=${redirect}&scope=code&code_challenge=${challenge}&code_challenge_method=S256`
            const authUrl = `http://localhost:8080/oauth/authorize?response_type=authorization_code&client_id=client1&code_challange=${challenge}&code_challenge_method=256&`
            window.location.href = authUrl
        }
        load()
    }, []);
    
    return (
        <div>
            <h1>Login</h1>
        </div>
    );
}

export async function createPKCE() {
    const array = new Uint8Array(32)
    crypto.getRandomValues(array)

    const verifier = base64UrlEncode(array)

    const hash = await crypto.subtle.digest(
        "SHA-256",
        new TextEncoder().encode(verifier)
    )

    const challenge = base64UrlEncode(new Uint8Array(hash))

    return { verifier, challenge }
}

function base64UrlEncode(buf) {
    return btoa(String.fromCharCode(...buf))
        .replace(/\+/g, "-")
        .replace(/\//g, "_")
        .replace(/=/g, "")
}