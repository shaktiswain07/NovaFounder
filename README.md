# ✦ NovaFounder

Describe a raw startup idea. Get back a full venture dossier — positioning,
market analysis, tech plan, database design, roadmap, budget, go-to-market
strategy, and an investor pitch — grounded in your real budget, timeline, and
team size.

```
Your idea + industry + audience + budget + timeline + team size
        ↓
🎯 The Vision   — Name, Tagline, Executive Summary, Problem, Solution, Target Users
🧭 The Market   — Competitor Analysis, Revenue Model, Go-to-Market Strategy
🛠️ The Build    — MVP Features, Tech Stack, DB Design, APIs, Folder Structure, Roadmap
💸 The Ask      — Cost Estimation, Investor Pitch, Resume Description
```

Built with Flask, the Groq API, HTML, CSS, and JavaScript.

## Setup

1. **Get a free Groq API key**
   Go to https://console.groq.com/keys, sign in, and create a key.

2. **Install dependencies**
   ```bash
   python -m venv venv
   source venv/bin/activate        # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Add your key**
   Open `.env` (already created from `.env.example`) and paste your key:
   ```
   GROQ_API_KEY=your_actual_key_here
   ```

4. **Run it**
   ```bash
   python app.py
   ```
   Visit http://127.0.0.1:5000

## How it flows

```
index.html "Launch the console" button
        ↓
GET /generator  →  generator.html (6-field input form)
        ↓
POST /generate  →  services/ai_service.py builds a prompt (prompts/prompt.py)
        ↓
Groq API (llama-3.3-70b-versatile) returns a 17-field structured JSON dossier
        ↓
result.html renders it as a dashboard: sticky sidebar nav grouped into
The Vision / The Market / The Build / The Ask, with copy buttons on the
pitch + resume description, and a client-side "Export PDF" button.
```

## Design notes

- The visual language (deep indigo background, "nova" coral-to-violet
  gradient, Space Grotesk + Inter + JetBrains Mono type system) lives
  entirely in `static/css/style.css`, built around CSS custom properties.
  It needs a modern browser (Chrome, Firefox, Safari, Edge — anything from
  the last several years); it will not render correctly in very old
  WebKit-based tools.
- PDF export happens client-side via jsPDF (loaded from a CDN in
  `result.html`) — no server-side PDF dependency required.
- `static/css/utils/pdf_generator.py` is an unused placeholder left over
  from before the redesign; safe to delete or repurpose for a server-side
  export later.

## Notes

- If `GROQ_API_KEY` is missing or invalid, the generator page shows an
  inline error instead of crashing.
- Model can be changed via the `GROQ_MODEL` env var (see `.env.example`).
