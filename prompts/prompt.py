"""
Prompt templates for NovaFounder.
Kept separate from services/ai_service.py so the wording can be tuned
without touching the API-calling logic.
"""


def build_prompt(idea, industry, audience, budget, timeline, team_size):
    """
    Build the user-facing prompt sent to the Groq model.

    idea:       str  raw startup idea, e.g. "AI that reviews rental leases for tenants"
    industry:   str  e.g. "PropTech"
    audience:   str  e.g. "Renters in the US"
    budget:     str  e.g. "$1,000 - $5,000"
    timeline:   str  e.g. "3 Months"
    team_size:  str  e.g. "Solo Founder"
    """
    return f"""You are a senior startup advisor and technical co-founder who has
helped launch dozens of early-stage companies. A founder has brought you a raw
idea. Turn it into a complete, realistic venture dossier.

Raw idea: {idea}
Industry: {industry}
Target audience: {audience}
Budget available: {budget}
Timeline to launch: {timeline}
Team size: {team_size}

Be specific and realistic — grounded in the budget, timeline, and team size
given. Favor a lean, buildable MVP over an over-scoped vision. Do not use
generic filler; every section should read as if you actually thought about
this specific idea.

Respond with ONLY a valid JSON object (no markdown fences, no commentary)
matching exactly this shape:

{{
  "startup_name": "A specific, brandable name (not generic)",
  "tagline": "One punchy sentence, under 12 words",
  "executive_summary": "3-4 sentences: what it is, who it's for, why now",
  "problem_statement": "2-3 sentences on the specific, painful problem",
  "solution": "2-3 sentences on how this product solves it",
  "target_users": ["Persona 1: short description", "Persona 2: short description", "Persona 3: short description"],
  "competitor_analysis": [
    {{"name": "Real or realistic competitor name", "description": "what they do", "gap": "what they miss that this startup addresses"}},
    {{"name": "...", "description": "...", "gap": "..."}},
    {{"name": "...", "description": "...", "gap": "..."}}
  ],
  "revenue_model": ["Revenue stream 1 with rough pricing", "Revenue stream 2 with rough pricing"],
  "mvp_features": ["Feature 1", "Feature 2", "Feature 3", "Feature 4", "Feature 5"],
  "tech_stack": {{
    "frontend": ["Tech 1", "Tech 2"],
    "backend": ["Tech 1", "Tech 2"],
    "database": ["Tech 1"],
    "ai_ml": ["Tech 1"],
    "deployment": ["Tech 1", "Tech 2"]
  }},
  "database_design": "Plain-text description of the key tables/collections and their important fields",
  "api_suggestions": ["Service name - what it's used for", "Service name - what it's used for", "Service name - what it's used for"],
  "folder_structure": ["frontend/", "backend/", "backend/routes/", "backend/models/", "requirements.txt", "README.md"],
  "roadmap": [
    {{"phase": "Phase name matching the given timeline", "tasks": "What gets built/done in this phase"}},
    {{"phase": "...", "tasks": "..."}},
    {{"phase": "...", "tasks": "..."}}
  ],
  "cost_estimation": {{
    "items": [
      {{"item": "Cost category (e.g. Hosting, Domain, AI API costs)", "estimate": "$X/month or $X one-time"}},
      {{"item": "...", "estimate": "..."}},
      {{"item": "...", "estimate": "..."}},
      {{"item": "...", "estimate": "..."}}
    ],
    "total_estimate": "Realistic total range given the stated budget"
  }},
  "go_to_market": ["GTM tactic 1, specific to this audience", "GTM tactic 2", "GTM tactic 3"],
  "investor_pitch": "A tight 4-6 sentence elevator pitch a founder could say out loud in 30 seconds: hook, problem, solution, market size or traction angle, ask.",
  "resume_description": "1-2 punchy resume bullet sentences starting with an action verb, mentioning the tech stack and role."
}}"""


SYSTEM_PROMPT = (
    "You are a precise assistant that only responds with valid JSON. "
    "Never include markdown code fences or any text outside the JSON object. "
    "Never leave a field generic or empty - every field must reflect the specific idea given."
)
