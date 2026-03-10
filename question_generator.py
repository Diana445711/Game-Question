import json
import re
from typing import Any

from gemini_client import get_gemini_client


QUESTION_SCHEMA_RULES = """
Return ONLY valid JSON. No markdown. No extra text.

JSON schema:
{
  "topic": "string",
  "difficulty": "easy|medium|hard",
  "question": "string",
  "choices": ["string", "string", "string", "string"],
  "answer_index": 0,
  "explanation": "string"
}

Rules:
- choices must contain exactly 4 options
- answer_index must be 0,1,2,or 3
- question must be one sentence
- explanation must be one short sentence
"""


def _extract_json(text: str) -> str:
    text = text.strip()

    match = re.search(r"\{.*\}", text, flags=re.DOTALL)

    if not match:
        raise ValueError("Could not extract JSON from model response")

    return match.group(0)


def generate_mcq(topic: str, difficulty: str) -> dict[str, Any]:

    client, model = get_gemini_client()

    prompt = f"""
You generate math multiple choice questions for a snakes and ladders educational game.

Topic: {topic}
Difficulty: {difficulty}

{QUESTION_SCHEMA_RULES}
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    raw = (response.text or "").strip()

    json_str = _extract_json(raw)

    data = json.loads(json_str)

    _validate_question(data)

    return data


def _validate_question(data: dict[str, Any]):

    required = [
        "topic",
        "difficulty",
        "question",
        "choices",
        "answer_index",
        "explanation",
    ]

    for k in required:
        if k not in data:
            raise ValueError(f"Missing field {k}")

    if len(data["choices"]) != 4:
        raise ValueError("Must have 4 choices")

    if data["answer_index"] not in [0, 1, 2, 3]:
        raise ValueError("answer_index must be 0-3")