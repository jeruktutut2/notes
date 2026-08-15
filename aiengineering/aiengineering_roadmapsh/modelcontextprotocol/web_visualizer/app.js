document.addEventListener('DOMContentLoaded', () => {
    // --- 1. NAV TABS SWITCHING ---
    const navButtons = document.querySelectorAll('.nav-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    navButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            navButtons.forEach(b => b.classList.remove('active'));
            tabContents.forEach(t => t.classList.remove('active'));

            btn.classList.add('active');
            const targetTab = btn.getAttribute('data-tab');
            document.getElementById(targetTab).classList.add('active');
        });
    });

    // --- 2. ARCHITECTURE DIAGRAM INTERACTIVE CARDS ---
    const componentDetails = {
        'host': {
            title: '🖥️ MCP Host',
            desc: 'MCP Host adalah aplikasi container utama tempat LLM beroperasi (seperti Claude Desktop, VS Code, Cursor, atau aplikasi AI Agent custom). Host mengelola koneksi client, izin pengguna, dan antarmuka interaksi.',
            code: `// Contoh Konfigurasi MCP Host (claude_desktop_config.json)
{
  "mcpServers": {
    "system-tools": {
      "command": "python3",
      "args": ["-m", "mcp_server"]
    }
  }
}`
        },
        'client': {
            title: '🔗 MCP Client',
            desc: 'MCP Client adalah modul internal yang mengelola 1:1 stateful connection dengan satu MCP Server. Bertanggung jawab atas negosiasi protokol JSON-RPC 2.0, inisialisasi, dan pengiriman request.',
            code: `async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()`
        },
        'server': {
            title: '⚙️ MCP Server',
            desc: 'MCP Server adalah program terisolasi yang menyediakan kapabilitas kontekstual (Resources, Prompts, dan Tools) untuk aplikasi LLM melalui protokol standar.',
            code: `mcp = FastMCP("My Server")

@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b`
        },
        'datalayer': {
            title: '📦 Data Layer Primitives',
            desc: 'Data Layer terdiri dari 3 primitif utama:\n• Resources: URI Data Read-only\n• Prompts: Templat Instruksi Reusable\n• Tools: Fungsi Eksekutabel Berdampak Samping',
            code: `Resources: file:///data.json, config://metrics
Prompts  : code_review(language="python")
Tools    : execute_query(sql="SELECT *")`
        },
        'transport': {
            title: '📡 Transport Layer',
            desc: 'Transport Layer membungkus pesan JSON-RPC 2.0. Mendukung Stdio Transport (subprocess IPC lokal via stdin/stdout) dan SSE / HTTP Transport (Server-Sent Events untuk koneksi remote web).',
            code: `Stdio Framing: {"jsonrpc":"2.0", ...}\\n
SSE Framing  : event: message\\ndata: {...}\\n\\n`
        },
        'build-server': {
            title: '🏗️ Building an MCP Server',
            desc: 'Proses mendefinisikan server MCP: mendaftarkan handler resources/list, resources/read, prompts/list, prompts/get, tools/list, dan tools/call.',
            code: `from mcp.server.fastmcp import FastMCP
server = FastMCP("Production Server")`
        },
        'build-client': {
            title: '🤖 Building an MCP Client',
            desc: 'Proses membangun client MCP yang menginisialisasi jabat tangan (initialize), menegosiasikan kapabilitas, menemukan daftar alat, dan memanggil fungsi.',
            code: `init_payload = {
  "jsonrpc": "2.0", "id": 1,
  "method": "initialize",
  "params": {"clientInfo": {"name": "MyClient", "version": "1.0"}}
}`
        },
        'connect-local': {
            title: '💻 Connect to Local Server',
            desc: 'Menghubungkan client ke server lokal menggunakan subprocess stdio transport dengan isolasi penuh di mesin lokal.',
            code: `server_params = StdioServerParameters(
    command="python3", args=["server.py"]
)`
        },
        'connect-remote': {
            title: '🌐 Connect to Remote Server',
            desc: 'Menghubungkan client ke server remote di cloud menggunakan SSE (Server-Sent Events) over HTTP/HTTPS dengan otentikasi Bearer Token.',
            code: `url = "https://api.example.com/sse"
headers = {"Authorization": "Bearer TOKEN"}`
        }
    };

    const cards = document.querySelectorAll('.interactive-card');
    const detailTitle = document.getElementById('detail-title');
    const detailDesc = document.getElementById('detail-desc');
    const detailExtra = document.getElementById('detail-extra');

    cards.forEach(card => {
        card.addEventListener('click', () => {
            cards.forEach(c => c.classList.remove('active-card'));
            card.classList.add('active-card');

            const key = card.getAttribute('data-component');
            const data = componentDetails[key];
            if (data) {
                detailTitle.textContent = data.title;
                detailDesc.textContent = data.desc;
                detailExtra.innerHTML = `<pre><code>${escapeHtml(data.code)}</code></pre>`;
            }
        });
    });

    // --- 3. LIVE JSON-RPC INSPECTOR ---
    const presets = {
        'initialize': {
            jsonrpc: "2.0",
            id: 1,
            method: "initialize",
            params: {
                protocolVersion: "2024-11-05",
                capabilities: { roots: { listChanged: true } },
                clientInfo: { name: "WebVisualizerInspector", version: "1.0.0" }
            }
        },
        'notifications_initialized': {
            jsonrpc: "2.0",
            method: "notifications/initialized"
        },
        'resources_list': {
            jsonrpc: "2.0",
            id: 2,
            method: "resources/list"
        },
        'resources_read': {
            jsonrpc: "2.0",
            id: 3,
            method: "resources/read",
            params: { uri: "notes://readme.md" }
        },
        'prompts_list': {
            jsonrpc: "2.0",
            id: 4,
            method: "prompts/list"
        },
        'tools_list': {
            jsonrpc: "2.0",
            id: 5,
            method: "tools/list"
        },
        'tools_call': {
            jsonrpc: "2.0",
            id: 6,
            method: "tools/call",
            params: {
                name: "calculate_expr",
                arguments: { expression: "125 * 8 + 50" }
            }
        },
        'ping': {
            jsonrpc: "2.0",
            id: 7,
            method: "ping"
        }
    };

    const presetButtons = document.querySelectorAll('.preset-btn');
    const jsonReqInput = document.getElementById('json-request-input');
    const jsonResOutput = document.getElementById('json-response-output');
    const sendBtn = document.getElementById('send-jsonrpc-btn');
    const inspectorLogs = document.getElementById('inspector-logs');

    // Load initial preset
    jsonReqInput.value = JSON.stringify(presets['initialize'], null, 2);

    presetButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            presetButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const reqKey = btn.getAttribute('data-req');
            if (presets[reqKey]) {
                jsonReqInput.value = JSON.stringify(presets[reqKey], null, 2);
            }
        });
    });

    sendBtn.addEventListener('click', () => {
        try {
            const reqObj = JSON.parse(jsonReqInput.value);
            logInspector(`OUTBOUND (${reqObj.method || 'notification'}): ${JSON.stringify(reqObj)}`, 'outbound');

            // Simulated Server Response Engine
            setTimeout(() => {
                const resObj = simulateServerProcessing(reqObj);
                if (resObj) {
                    jsonResOutput.textContent = JSON.stringify(resObj, null, 2);
                    logInspector(`INBOUND (ID ${reqObj.id}): Result received cleanly!`, 'inbound');
                } else {
                    jsonResOutput.textContent = "// Notification Sent (No Result Frame Expected)";
                    logInspector(`NOTIFICATION ACKNOWLEDGED`, 'inbound');
                }
            }, 300);
        } catch (err) {
            alert('Format JSON Request tidak valid: ' + err.message);
        }
    });

    function logInspector(msg, type) {
        const item = document.createElement('div');
        item.className = `log-item ${type}`;
        item.textContent = `[${new Date().toLocaleTimeString()}] ${msg}`;
        inspectorLogs.appendChild(item);
        inspectorLogs.scrollTop = inspectorLogs.scrollHeight;
    }

    function simulateServerProcessing(req) {
        const id = req.id;
        const method = req.method;

        if (method === "initialize") {
            return {
                jsonrpc: "2.0",
                id: id,
                result: {
                    protocolVersion: "2024-11-05",
                    capabilities: {
                        resources: { subscribe: true, listChanged: true },
                        prompts: { listChanged: true },
                        tools: { listChanged: true }
                    },
                    serverInfo: { name: "Simulated-MCP-Web-Server", version: "1.0.0" }
                }
            };
        } else if (method === "notifications/initialized") {
            return null;
        } else if (method === "resources/list") {
            return {
                jsonrpc: "2.0",
                id: id,
                result: {
                    resources: [
                        { uri: "notes://readme.md", name: "readme.md", mimeType: "text/plain" },
                        { uri: "config://system-metrics", name: "system-metrics", mimeType: "application/json" }
                    ]
                }
            };
        } else if (method === "resources/read") {
            return {
                jsonrpc: "2.0",
                id: id,
                result: {
                    contents: [{
                        uri: req.params.uri,
                        mimeType: "text/plain",
                        text: "# Project Roadmap\n1. Connect MCP Server\n2. Run AI Agent"
                    }]
                }
            };
        } else if (method === "prompts/list") {
            return {
                jsonrpc: "2.0",
                id: id,
                result: {
                    prompts: [{ name: "code_review", description: "Standard AI Code Review Prompt" }]
                }
            };
        } else if (method === "tools/list") {
            return {
                jsonrpc: "2.0",
                id: id,
                result: {
                    tools: [
                        { name: "calculate_expr", description: "Evaluates math expression" },
                        { name: "write_note", description: "Writes text to URI" }
                    ]
                }
            };
        } else if (method === "tools/call") {
            const expr = req.params?.arguments?.expression || "10 + 10";
            let val = 1050;
            try { val = eval(expr); } catch (e) {}
            return {
                jsonrpc: "2.0",
                id: id,
                result: {
                    content: [{ type: "text", text: `Hasil Kalkulasi (${expr}) = ${val}` }],
                    isError: false
                }
            };
        } else if (method === "ping") {
            return { jsonrpc: "2.0", id: id, result: {} };
        } else {
            return {
                jsonrpc: "2.0",
                id: id,
                error: { code: -32601, message: `Method '${method}' not supported` }
            };
        }
    }

    // --- 4. HOST-CLIENT-SERVER SANDBOX ---
    const runAgentBtn = document.getElementById('run-agent-loop-btn');
    const userPromptInput = document.getElementById('user-prompt-input');
    const agentThought = document.getElementById('agent-thought');
    const sandboxExecLog = document.getElementById('sandbox-execution-log');

    runAgentBtn.addEventListener('click', () => {
        const query = userPromptInput.value.trim();
        sandboxExecLog.innerHTML = '';
        
        appendSandboxLog(`🤖 User Query: "${query}"`, 'normal');
        agentThought.innerHTML = `<em>Thinking: Mengurai kebutuhan pengguna... Menemukan kebutuhan kalkulasi (50 * 12 + 100) dan pembacaan resource 'notes://readme.md'.</em>`;

        setTimeout(() => {
            appendSandboxLog(`[MCP CLIENT] ➔ Sending 'resources/read' for URI 'notes://readme.md'`, 'tool');
        }, 500);

        setTimeout(() => {
            appendSandboxLog(`[MCP SERVER] ⬅️ Returned Resource Content: "# Project Roadmap\\n1. Integrasi MCP..."`, 'result');
        }, 1000);

        setTimeout(() => {
            appendSandboxLog(`[MCP CLIENT] ➔ Sending 'tools/call' (calculate_expr) args: {"expression": "50 * 12 + 100"}`, 'tool');
        }, 1500);

        setTimeout(() => {
            appendSandboxLog(`[MCP SERVER] ⬅️ Tool Result: "Hasil Kalkulasi (50 * 12 + 100) = 700"`, 'result');
        }, 2000);

        setTimeout(() => {
            appendSandboxLog(`✨ LLM Final Response Generated:\n"Hasil perhitungan 50 * 12 + 100 adalah 700. Catatan roadmap proyek berisi poin integrasi MCP."`, 'result');
            agentThought.innerHTML = `<em>Status: Selesai mengeksekusi LLM Agent Loop dengan sukses!</em>`;
        }, 2500);
    });

    function appendSandboxLog(text, styleClass) {
        const line = document.createElement('div');
        line.className = `log-line ${styleClass}`;
        line.textContent = text;
        sandboxExecLog.appendChild(line);
        sandboxExecLog.scrollTop = sandboxExecLog.scrollHeight;
    }

    // --- 5. TRANSPORTS SIMULATOR ---
    const simStdioBtn = document.getElementById('sim-stdio-btn');
    const stdioPreview = document.getElementById('stdio-frame-preview');
    const simSseBtn = document.getElementById('sim-sse-btn');
    const ssePreview = document.getElementById('sse-frame-preview');

    simStdioBtn.addEventListener('click', () => {
        stdioPreview.textContent = '{"jsonrpc":"2.0","id":101,"method":"tools/list"}\\n';
    });

    simSseBtn.addEventListener('click', () => {
        ssePreview.textContent = 'event: message\ndata: {"jsonrpc":"2.0","method":"notifications/resources/updated","params":{"uri":"notes://readme.md"}}\n\n';
    });

    // --- 6. DEVELOPER GUIDE CODE DISPLAY ---
    const guideCodes = {
        'server-code': `from mcp.server.fastmcp import FastMCP

# 1. Inisialisasi FastMCP Server
mcp = FastMCP("My Custom Server")

# 2. Definisikan Resource
@mcp.resource("config://app")
def get_config() -> str:
    return '{"status": "active"}'

# 3. Definisikan Tool
@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Mengalikan dua bilangan bulat."""
    return a * b

if __name__ == "__main__":
    mcp.run()`,

        'client-code': `import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(command="python3", args=["server.py"])
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("multiply", {"a": 6, "b": 7})
            print("Hasil Tool:", result.content)

asyncio.run(main())`,

        'local-code': `# Konfigurasi Local Stdio Server di Claude Desktop / MCP Host
{
  "mcpServers": {
    "sqlite-db": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "~/test.db"]
    }
  }
}`,

        'remote-code': `import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client

async def connect_remote():
    url = "https://mcp-server.example.com/sse"
    headers = {"Authorization": "Bearer SECRET_KEY"}
    async with sse_client(url, headers=headers) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("Connected to Remote SSE Server!")

asyncio.run(connect_remote())`
    };

    const guideButtons = document.querySelectorAll('.guide-tab-btn');
    const guideCodeDisplay = document.getElementById('guide-code-display');

    // Initial guide code
    guideCodeDisplay.textContent = guideCodes['server-code'];

    guideButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            guideButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            const codeKey = btn.getAttribute('data-guide');
            if (guideCodes[codeKey]) {
                guideCodeDisplay.textContent = guideCodes[codeKey];
            }
        });
    });

    function escapeHtml(str) {
        return str.replace(/&/g, "&amp;")
                  .replace(/</g, "&lt;")
                  .replace(/>/g, "&gt;")
                  .replace(/"/g, "&quot;")
                  .replace(/'/g, "&#039;");
    }
});
