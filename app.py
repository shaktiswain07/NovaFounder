from flask import Flask, render_template, request
from services.ai_service import generate_startup

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/generator")
def generator():
    return render_template("generator.html")


@app.route("/generate", methods=["POST"])
def generate():

    idea = request.form.get("idea", "").strip()
    industry = request.form.get("industry", "").strip()
    audience = request.form.get("audience", "").strip()
    budget = request.form.get("budget", "").strip()
    timeline = request.form.get("timeline", "").strip()
    team_size = request.form.get("team_size", "").strip()

    if not idea or not industry:
        return render_template(
            "generator.html",
            error="Please describe your idea and select an industry.",
            form=request.form,
        )

    startup = generate_startup(
        idea,
        industry,
        audience,
        budget,
        timeline,
        team_size,
    )

    if "error" in startup:
        return render_template(
            "generator.html",
            error=startup["error"],
            form=request.form,
        )

    return render_template(
        "result.html",
        s=startup,
        inputs={
            "idea": idea,
            "industry": industry,
            "audience": audience,
            "budget": budget,
            "timeline": timeline,
            "team_size": team_size,
        },
    )


if __name__ == "__main__":
    app.run(debug=True)
