# VibeCoders United: Design & Branding Identity

**VibeCoders United** is the overarching organization. Our product is a **standalone IDE application** (similar to commercial standalone AI IDEs)—built entirely from **open-source projects** that can be pulled and built from GitHub. No vendor lock-in; full control and community ownership.

---

## 🎨 The Aesthetic: "Scarlet & Jade"

Accent colours are **Scarlet** and **Jade**, with **complementary neutral tones** that keep the focus on the accents. The result is bold, recognizable, and easy on the eyes.

### 🌓 The Color Palette: "Scarlet, Jade & Neutrals"

- **Accent – Scarlet**: `#C41E3A` (primary scarlet) — Actions, warnings, emphasis, and "manual override" states.
- **Accent – Jade**: `#0D9488` (jade/teal) — Success, "agent running," indexing complete, and positive feedback.
- **Neutral base (dark)**: `#1C1917` (Stone 900) — Main background; warm neutral that makes scarlet and jade stand out.
- **Neutral surface**: `#292524` (Stone 800) — Panels, sidebars, and elevated surfaces.
- **Neutral muted**: `#57534E` (Stone 500) — Borders, secondary text, and subtle UI.
- **Neutral highlight**: `#F5F5F4` (Stone 100) — Primary text on dark; ensures readability.
- **Glassmorphism**: 12–15% opacity overlays with `backdrop-filter: blur(20px)` for floating panels so accents stay visible.

Use **Scarlet** for primary CTAs and critical states; use **Jade** for success, progress, and AI/agent activity. Neutrals carry the rest of the UI.

**Design tokens (copy-paste):**

| Token        | Hex       | Use                    |
|-------------|-----------|------------------------|
| `--accent-scarlet` | `#C41E3A` | Primary actions, warnings |
| `--accent-jade`    | `#0D9488` | Success, agent, indexing  |
| `--neutral-base`   | `#1C1917` | Main background          |
| `--neutral-surface`| `#292524` | Panels, sidebars          |
| `--neutral-muted`  | `#57534E` | Borders, secondary text  |
| `--neutral-highlight` | `#F5F5F4` | Primary text on dark  |

### ⌨️ Typography: "Variable Brutalism"

- **UI Font**: `JetBrains Mono` or `Inter Variable` (high contrast, tight tracking).
- **Code Font**: `Berkeley Mono` or `Input Mono` (custom ligatures, optimized for code).

---

## 🏗️ UI Components: "The Bento Shell"

The IDE uses a **Bento Grid** layout for metadata; the editor remains the main canvas.

1. **The Ghost Terminal**: Semi-transparent overlay at the bottom showing AI "thinking" and logs in real time. Neutrals for background; Jade for active/streaming state.
2. **The Context Orb**: Status bar indicator that changes colour by indexing state — **Jade** = fully indexed, **Scarlet** = needs attention or manual override, neutral = indexing or idle.
3. **The Shadow Diff**: Changes appear as subtle "ghost" text with a soft glow (Jade tint for additions, Scarlet tint for removals where appropriate), fading in when the AI proposes an edit.

---

## ⚡ The Vibe: "High-Agency & Transparent"

- **Tactile feedback**: Low-frequency clicks when the AI accepts a goal; no high-pitched beeps.
- **Terminal first**: All AI actions are logged in a History tab that feels like a flight recorder.
- **No mystery**: Every "magic" action has a "Show Source" button revealing the exact prompt and context.

---

## 🏢 Organization & Product

| | |
|---|---|
| **Organization** | **VibeCoders United** |
| **Product** | Standalone IDE application (single-product experience) |
| **Foundation** | Open-source projects; pull and build from GitHub |
| **Mission** | World-class AI coding without vendor lock-in or hidden telemetry |

---

*"Coding is no longer about writing lines; it's about directing a symphony of agents. VibeCoders United is your baton."*
