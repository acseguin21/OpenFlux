import { useState, useCallback } from "react"

const DEFAULT_BACKEND = "http://localhost:8000"

type Message = { role: "user" | "assistant"; content: string }

export default function App() {
  const [backendUrl, setBackendUrl] = useState(DEFAULT_BACKEND)
  const [connected, setConnected] = useState<boolean | null>(null)
  const [composerText, setComposerText] = useState("")
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)

  const checkBackend = useCallback(async () => {
    setConnected(null)
    try {
      const base = backendUrl.replace(/\/$/, "")
      const res = await fetch(`${base}/`, { method: "GET" })
      setConnected(res.ok)
    } catch {
      setConnected(false)
    }
  }, [backendUrl])

  const sendGoal = useCallback(async () => {
    const text = composerText.trim()
    if (!text || !connected || loading) return
    setMessages((prev) => [...prev, { role: "user", content: text }])
    setComposerText("")
    setLoading(true)
    try {
      const base = backendUrl.replace(/\/$/, "")
      const res = await fetch(`${base}/api/agent/execute`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          goal: text,
          workspace_path: ".", // desktop may not have a workspace; backend can use cwd or prompt
          max_iterations: 5,
        }),
      })
      const data = await res.json().catch(() => ({}))
      const msg =
        data.message ??
        (res.ok ? "Request completed." : `Error: ${res.status} ${res.statusText}`)
      setMessages((prev) => [...prev, { role: "assistant", content: msg }])
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `Error: ${e instanceof Error ? e.message : String(e)}` },
      ])
    } finally {
      setLoading(false)
    }
  }, [backendUrl, composerText, connected, loading])

  return (
    <div className="app">
      <h1>OpenFlux</h1>
      <p className="tagline">Connect to your OpenFlux backend to use the agent.</p>

      <div className="connect-bar">
        <input
          type="url"
          value={backendUrl}
          onChange={(e) => setBackendUrl(e.target.value)}
          placeholder="Backend URL"
          aria-label="Backend URL"
        />
        <button type="button" className="primary" onClick={checkBackend}>
          Connect
        </button>
      </div>

      {connected !== null && (
        <div className={`status ${connected ? "connected" : "disconnected"}`}>
          {connected ? "Connected" : "Backend unreachable. Start it with: ./scripts/start_server.sh"}
        </div>
      )}

      <div className="composer">
        <textarea
          value={composerText}
          onChange={(e) => setComposerText(e.target.value)}
          placeholder="Describe what you want the agent to do..."
          disabled={!connected || loading}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault()
              sendGoal()
            }
          }}
        />
        <div className="composer-actions">
          <button
            type="button"
            onClick={sendGoal}
            disabled={!connected || loading || !composerText.trim()}
          >
            {loading ? "Running…" : "Run agent"}
          </button>
        </div>
      </div>

      {messages.length > 0 && (
        <div className="chat-log">
          {messages.map((m, i) => (
            <div key={i} className={`message ${m.role}`}>
              <div className="role">{m.role === "user" ? "You" : "OpenFlux"}</div>
              <div className="content">{m.content}</div>
            </div>
          ))}
        </div>
      )}

      <p className="footer-note">
        Start the backend from the repo root: <code>./scripts/start_server.sh</code>
      </p>
    </div>
  )
}
