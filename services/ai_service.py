import os
import json
from groq import Groq
from dotenv import load_dotenv
from prompts.prompt import build_prompt, SYSTEM_PROMPT

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")

# Client is created lazily so importing this module doesn't crash
# if GROQ_API_KEY isn't set yet (e.g. during setup).
_client = None


def _get_client():
    global _client
    if _client is None:
        if not GROQ_API_KEY:
            raise RuntimeError(
                "GROQ_API_KEY is not set. Copy .env.example to .env and add your key "
                "from https://console.groq.com/keys"
            )
        _client = Groq(api_key=GROQ_API_KEY)
    return _client


def generate_startup(idea, industry, audience, budget, timeline, team_size):
    """
    Calls Groq to turn a raw startup idea into a full venture dossier.
    Returns a dict on success, or a dict with an "error" key on failure
    (callers/templates should check for "error" before rendering).
    """
    prompt = build_prompt(idea, industry, audience, budget, timeline, team_size)

    try:
        client = _get_client()
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.85,
            response_format={"type": "json_object"},
        )
        raw_text = response.choices[0].message.content
        startup = json.loads(raw_text)
        return startup

    except RuntimeError as e:
        # Missing API key
        return {"error": str(e)}
    except json.JSONDecodeError:
        return {"error": "The AI returned a response that wasn't valid JSON. Try generating again."}
    except Exception as e:
        # Covers network errors, auth errors (401), rate limits (429), etc.
        return {"error": f"Could not generate startup: {e}"}
