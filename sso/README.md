# SSO

## Workflow
    Flow SSO standar (OAuth2 / OpenID Connect style)
    1️⃣ User akses app1.com
    GET https://app1.com/dashboard
    app1 cek cookie/session
    ❌ belum login

    2️⃣ app1 redirect ke auth
    302 Found
    Location: https://auth.company.com/login?
      client_id=app1
      &redirect_uri=https://app1.com/callback
      &state=xyz123
    
    📌 auth BELUM tahu user siapa
    Yang auth tahu baru:
    - ini request dari app1
    - mau balik ke app1
    - ada state untuk anti-CSRF

    3️⃣ User login di auth
    POST https://auth.company.com/login
    (email + password / SSO Google / dll)

    Sekarang auth:
    ✅ tahu user siapa
    bikin session cookie auth
    auth_session=abc123
    Domain=auth.company.com
    HttpOnly
    Secure

    4️⃣ auth redirect ke app1 + code
    302 Found
    Location: https://app1.com/callback?
      code=authcode123
      &state=xyz123
    
    📌 Yang dikirim BUKAN cookie, tapi authorization code
    5️⃣ app1 verifikasi ke auth (SERVER-TO-SERVER)
    POST https://auth.company.com/token
    code=AUTH_CODE_789
    client_secret=...
    Auth jawab:

    {
      "user_id": "u-123",
      "email": "user@mail.com",
      "access_token": "jwt..."
    }

    ➡️ app1 sekarang:
    tahu user siapa
    set cookie milik app1.com sendiri