import google.generativeai as genai
from app.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={
        "temperature": 0.3,
        "response_mime_type": "application/json"
    }
)

def decompose_task(title: str, deadline_str: str) -> list:
    prompt = f"""
You are a productivity expert. Break down the following task into clear, actionable subtasks.

Task: "{title}"
Deadline: {deadline_str}

Rules:
- Generate 3 to 6 subtasks maximum
- Each subtask must be concrete and completable in one sitting
- Estimate realistic time in minutes for each subtask
- Order them logically (what to do first, second, etc.)

Respond ONLY with a JSON array in this exact format, nothing else:
[
  {{"title": "subtask description", "est_minutes": 30, "order": 1}},
  {{"title": "subtask description", "est_minutes": 45, "order": 2}}
]
"""
    response = model.generate_content(prompt)
    import json
    return json.loads(response.text)


def calculate_risk_score(title: str, deadline_str: str, total_minutes: int) -> float:
    prompt = f"""
You are a deadline risk analyzer.

Task: "{title}"
Deadline: {deadline_str}
Total estimated time needed: {total_minutes} minutes

Analyze the risk of missing this deadline on a scale of 0.0 to 1.0.
- 0.0 means plenty of time, very low risk
- 1.0 means deadline is extremely tight or already passed, very high risk

Respond ONLY with a JSON object in this exact format, nothing else:
{{"risk_score": 0.75}}
"""
    response = model.generate_content(prompt)
    import json
    result = json.loads(response.text)
    return result["risk_score"]