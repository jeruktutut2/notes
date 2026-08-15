document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault(); // Mencegah refresh halaman

    // Mengambil data dari input
    const email = document.getElementById('email').value
    const password = document.getElementById('password').value;

    const payload = {
        email: email,
        password: password
    };

    try {
        // Mengirim data ke /loginui
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        // Menampilkan hasil (karena /loginui mungkin belum ada, ini akan error 404)
        const responsejson = await response.json()
        if (response.ok) {
            document.getElementById('responseMessage').innerText = "Data Berhasil Terkirim!";
        } else if (response.redirected) {
            console.log("redirect")
            window.location.href = response.url;
            return;
        } else {
            document.getElementById('responseMessage').innerText = responsejson.errors.message
        }
    } catch (error) {
        document.getElementById('responseMessage').innerText = "Gagal menghubungi server.";
        console.error("Detail Error:", error);
    }
});