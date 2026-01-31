# What OpenFlux Can Learn from OpenCode

OpenCode (anomalyco/opencode) is an open-source AI coding agent modeled after **Claude Code** (terminal/TUI-first, multi-agent). OpenFlux is modeled after **Cursor** (IDE-first, editor + extension + backend). This document summarizes what we can learn from OpenCode to improve OpenFlux.

---

## 1. High-Level Comparison

| Aspect | OpenCode (Claude Code model) | OpenFlux (Cursor model) |
|--------|------------------------------|--------------------------|
| **Primary UX** | Terminal/TUI, desktop (Tauri), web | IDE (open editor base) + extension |
| **Stack** | TypeScript/Bun, monorepo (packages/opencode, app, desktop, sdk) | Python backend (FastAPI) + TS extension + shell |
| **Agents** | Two built-in: **build** (full access), **plan** (read-only, asks before bash) + **general** subagent | Single flow: plan → execute → verify |
| **Config** | `.opencode/` (opencode.jsonc, agent/, command/, skill/, tool/) | Minimal; backend env, extension settings |
| **Context** | AGENTS.md, CLAUDE.md, glob-up config; MCP + tools (codesearch, grep, etc.) | Tree-sitter + LanceDB indexer; orchestrator uses index search |
| **Permissions** | Explicit ask/allow/deny per tool/pattern (e.g. read .env, bash, external dirs) | Not yet (implicit trust) |
| **Session** | Project → Session → Message API; compaction, revert, share | Stateless API; no session persistence model |

---

## 2. Lessons and Recommended Improvements

### 2.1 Multi-Agent / Mode (Plan vs Build)

**What OpenCode does:**  
Two agents selectable (e.g. via Tab): **build** (default, can run tools and edit) and **plan** (read-only by default; denies edits, asks before running bash). A **general** subagent is used for complex search/multistep tasks (e.g. `@general`).

**Recommendation for OpenFlux:**  
- Add a **“Plan” or “Explore” mode** in the IDE: read-only by default (no direct file edits; suggestions or diffs only) and optional “ask before run” for terminal commands.  
- Keep current **“Build”/Agent mode** for full plan–execute–verify with edits.  
- Optionally support a **subagent** or “research” flow for heavy search/context-gathering without touching the main agent context.

**Where:** Extension (mode toggle), orchestrator (respect “plan” vs “build” when deciding to apply edits or run commands).

---

### 2.2 Project-Scoped Config (`.openflux/` or `.cursor`-style)

**What OpenCode does:**  
- `.opencode/opencode.jsonc`: provider, MCP servers, tool toggles.  
- `.opencode/agent/*.md`: agent definitions (mode, model, color, tools, permission overrides).  
- `.opencode/command/*.md`: command templates.  
- `.opencode/skill/*/SKILL.md`: repo-specific skills (e.g. “use Bun file APIs”).  
- `.opencode/tool/*.ts`: custom tools loaded at runtime.  
- Instruction prompt: AGENTS.md, CLAUDE.md from config dir and home; `globUp` for project root.

**Recommendation for OpenFlux:**  
- Introduce **project-level config** (e.g. `.openflux/config.jsonc` or reuse `.cursor` conventions):  
  - Provider / model preferences.  
  - Optional MCP server list.  
  - Feature toggles (e.g. which tools are on).  
- **Agent definitions**: optional `.openflux/agents/*.md` (or similar) to define “plan” vs “build” behavior and permissions.  
- **Skills**: support `.openflux/skills/*/SKILL.md` (or `.cursor/skills/`) so the model gets repo-specific rules (languages, style, APIs).  
- **Rules**: load `AGENTS.md` / `.cursor/rules` from workspace root so the orchestrator and extension share the same “project rules.”

**Where:** Backend and extension both read workspace root; orchestrator and extension use the same config/skills/rules.

---

### 2.3 Permission UX (Ask / Allow / Deny)

**What OpenCode does:**  
- **Permission** module: type (e.g. `read`, `bash`, `external_directory`), optional **pattern** (e.g. `*.env`, paths).  
- Rules: **allow** / **ask** / **deny**; merged from defaults and user config.  
- Session-scoped pending/approved; UI asks user before executing when permission is `ask`.

**Recommendation for OpenFlux:**  
- Define **permission types** (e.g. file_edit, read_env, run_bash, external_directory).  
- Support **patterns** (e.g. `*.env` = ask, `*.env.example` = allow).  
- In the IDE: when the agent wants to run a command or edit a sensitive file, **prompt the user** (allow once / allow for session / deny).  
- Persist “approved” state per session only (no long-term storage of approvals by default).

**Where:** Orchestrator (emit permission requests), extension (show approval UI), optional backend session state.

---

### 2.4 MCP (Model Context Protocol) Integration

**What OpenCode does:**  
- First-class **MCP** in config: remote (HTTP/SSE), stdio, with optional OAuth.  
- MCP tools and resources exposed to the agent; e.g. **codesearch** uses Exa MCP; **context7** in their sample config.  
- Events when MCP tools change; timeouts and auth handling.

**Recommendation for OpenFlux:**  
- Add **MCP client support** in the backend or extension: connect to remote/stdio MCP servers from config.  
- Expose MCP **tools** to the orchestrator so the agent can call “codesearch,” “context7,” or custom MCP tools.  
- Optional: MCP **resources** for large or dynamic context (e.g. docs) without stuffing everything into the main prompt.  
- Keep **BYOK** and **local-first**: MCP can be local-only (stdio) or user-configured remote.

**Where:** Backend (MCP client + tool registry) or extension (MCP client that forwards to backend); config in `.openflux` or settings.

---

### 2.5 Tool Ecosystem and Output Truncation

**What OpenCode does:**  
- Rich **tool set**: read, write, edit, multiedit, apply_patch, bash, glob, grep, codesearch, websearch, webfetch, LSP, skill, plan_enter/plan_exit, todo, question.  
- **Plugin** and **custom tool** dirs: load `tool/*.ts` and plugin tools from config directories.  
- **Truncation**: long tool output is truncated with a cap and optional path to full output (e.g. temp file) so the context window is not blown.

**Recommendation for OpenFlux:**  
- **Standardize tools** used by the orchestrator: read, write, edit, grep, glob, run_bash, LSP (if available).  
- Add **output truncation** in the backend: when a tool (or indexer) returns large content, truncate with a clear boundary and optionally store full result for follow-up (e.g. “read from path X”).  
- Optional: **plugin/custom tools** (e.g. from `.openflux/tools/` or extension) so power users can add project-specific tools.

**Where:** Orchestrator (tool registry, truncation helper), indexer (already chunks; ensure we don’t over-fill context).

---

### 2.6 Session and Project API

**What OpenCode does:**  
- **REST-ish API**: `GET/POST /project`, `GET/POST/DELETE /project/:id/session`, `GET/POST /project/:id/session/:id/message`, plus revert, share, compact, permission, file status.  
- **Spec** (specs/project.md): single instance can run sessions for multiple projects/worktrees.  
- Compaction and revert at session level.

**Recommendation for OpenFlux:**  
- **Session abstraction**: optional project/session/message model so the IDE (and future desktop/web clients) can support multiple workspaces and multiple agent sessions.  
- **Compaction**: summarize or drop old messages when context is too long (similar to OpenCode’s compaction).  
- **Revert**: optional “revert to message N” for the current session (restore file state or plan state).  
- Keep the current “stateless” API as the default; add session endpoints as an optional layer.

**Where:** Backend (new routes and session store), extension (use session ID when talking to backend).

---

### 2.7 Specs and Guardrails (Payload, Cache, Throttling)

**What OpenCode does:**  
- **Payload limits** (specs/01): avoid storing huge payloads in KV (e.g. localStorage); blob store for images; size caps and policies per key.  
- **Cache eviction** (specs/02): LRU + TTL + size caps for in-memory caches (sessions, messages, file contents).  
- **Request throttling** (specs/03): limit concurrent or frequent requests.  
- **Modularize and dedupe** (specs/05): scoped session cache utility, split mega-components into view/controller/services.

**Recommendation for OpenFlux:**  
- **Document** similar guardrails in `docs/specs/` (or equivalent): payload limits for any persisted state (e.g. draft, history), cache eviction for in-memory caches in the extension/backend, and throttling for LLM/API calls.  
- **Implement** where relevant: e.g. extension-side caps on stored prompt history or indexed blob size; backend cache eviction if we add in-memory caches.  
- **Modularize** the extension (session, composer, layout) with clear view/controller boundaries and shared scoped-cache utilities to avoid mega-components and unbounded growth.

**Where:** Docs (specs), extension (persist + caches), backend (if we add caches or queues).

---

### 2.8 AGENTS.md and Project Rules

**What OpenCode does:**  
- **AGENTS.md** at repo root (and config dir): style guide (single-word vars, avoid let/else, prefer Bun APIs), testing (no mocks, test real impl).  
- Instruction module **globs up** for AGENTS.md, CLAUDE.md so every project can drive agent behavior.

**Recommendation for OpenFlux:**  
- **Respect AGENTS.md / .cursor/rules** in the workspace: backend or extension reads them and injects into the orchestrator system prompt.  
- Optional: **CLAUDE.md** compatibility (e.g. from home or project) so users coming from Claude Code can reuse the same file.  
- Document in QUICKSTART/USAGE that “add AGENTS.md or .cursor/rules to your repo to tailor the agent.”

**Where:** Extension (discover workspace root), backend (accept “project rules” in index or agent request), orchestrator (prepend to system prompt).

---

### 2.9 Skills (SKILL.md)

**What OpenCode does:**  
- **Skills** in `.opencode/skill/*/SKILL.md`: frontmatter (name, description) + “Use this when” + guidelines (e.g. Bun file I/O, when to use node:fs).  
- Loaded and exposed to the agent so it follows repo-specific conventions.

**Recommendation for OpenFlux:**  
- Support **SKILL.md** in `.openflux/skills/` (or `.cursor/skills/`): name, description, “use when,” and short guidelines.  
- Backend (or extension) collects these and passes them as extra context or system snippets to the orchestrator.  
- Enables “in this repo we use Bun for file I/O” or “in this repo we use pytest only” without changing the core prompt.

**Where:** Workspace config discovery (extension or backend), orchestrator (inject skill text into context).

---

### 2.10 Testing and Style (AGENTS.md)

**What OpenCode does:**  
- **AGENTS.md** tells the AI: avoid mocks, test real implementation; prefer single-word names, const over let, early returns, Bun APIs where possible.

**Recommendation for OpenFlux:**  
- In our own **AGENTS.md** (or contributor docs): similar style and testing guidelines so AI-assisted contributions stay consistent.  
- For **user projects**: if AGENTS.md exists, we already recommend loading it (see 2.8); that can include project-specific testing and style rules.

**Where:** OpenFlux repo’s AGENTS.md or CONTRIBUTING; orchestrator uses project AGENTS.md when present.

---

## 3. Summary Table: Priorities

| Priority | Improvement | Effort | Impact |
|----------|-------------|--------|--------|
| High | Project rules (AGENTS.md / .cursor/rules) loaded into orchestrator | Low | High |
| High | Plan vs Build mode (read-only vs full edit) in IDE | Medium | High |
| High | Permission UX (ask before edit/run for sensitive paths) | Medium | High |
| Medium | .openflux/ config (provider, MCP, tool toggles) | Medium | Medium |
| Medium | MCP client (remote/stdio) and expose tools to agent | High | High |
| Medium | Session/project API (sessions, compaction, revert) | Medium | Medium |
| Medium | Output truncation and tool guardrails | Low–Medium | Medium |
| Low | Skills (SKILL.md) in workspace | Low | Medium |
| Low | Specs (payload, cache, throttle) and modularize UI | Ongoing | Medium |

---

## 4. References (OpenCode)

- **Agent definitions:** `packages/opencode/src/agent/agent.ts` (build, plan, defaults).  
- **Permission:** `packages/opencode/src/permission/index.ts` (Info, ask/allow/deny, session state).  
- **Instruction:** `packages/opencode/src/session/instruction.ts` (AGENTS.md, CLAUDE.md, globUp).  
- **Tools:** `packages/opencode/src/tool/registry.ts`, `tool/*.ts` (read, write, edit, bash, grep, codesearch, etc.).  
- **MCP:** `packages/opencode/src/mcp/index.ts` (client, remote/stdio/SSE, OAuth).  
- **Config:** `.opencode/opencode.jsonc`, `packages/opencode/src/config/config.ts`.  
- **Specs:** `specs/01-persist-payload-limits.md`, `02-cache-eviction.md`, `05-modularize-and-dedupe.md`, `specs/project.md`.  
- **Skills:** `.opencode/skill/bun-file-io/SKILL.md`, `packages/opencode/src/skill/skill.ts`.

Using this document, we can adopt the highest-value ideas (project rules, plan/build mode, permissions, MCP, session model, and guardrails) in phases without losing OpenFlux’s IDE-first, BYOK, and local-first identity.
