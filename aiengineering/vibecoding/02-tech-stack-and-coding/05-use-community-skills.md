# 05 - Use Skills & Tools Created by Others

## 🎯 Definisi & Konsep
**Use Skills Created by Others** adalah memanfaatkan ekosistem alat bantu (*custom skills*, Model Context Protocol / MCP, plugin, dan template prompt) yang dikembangkan oleh komunitas developer untuk memperluas kemampuan AI Coding Assistant.

Daripada mengajari AI tata cara atau sintaks kompleks dari nol, Anda dapat mengintegrasikan skill yang sudah teruji.

---

## 🛠️ Contoh Modalitas Skill Komunitas
1. **Agent Skills / Custom Instructions**: Berkas aturan khusus seperti `.cursorrules` dari repository open-source (misal cursor.directory).
2. **MCP (Model Context Protocol) Servers**: Server integrasi yang memungkinkan AI membaca database live, mengontrol browser (Playwright), memanggil API GitHub, atau mengeksekusi terminal.
3. **CLI Extension Tools**: Tool seperti `Claude Code`, `Github Copilot CLI`, atau Antigravity subagents.

---

## 💬 Contoh Penggunaan dalam Vibe Coding
```text
Saya telah menginstall Playwright MCP Server. 
Tolong gunakan skill browser automation ini untuk membuka http://localhost:3000, lakukan pengisian form login, dan beri tahu saya jika ada error visual di konsol browser.
```
