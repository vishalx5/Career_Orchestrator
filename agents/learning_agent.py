import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY")
)

def create_learning_pathway(missing_skills):

    if not missing_skills:
        return []

    prompt = f"""
You are a professional personalized learning advisor.

The candidate is missing the following skills:

{missing_skills}

Create a practical learning pathway to help the candidate develop
these skills.

For every missing skill, provide:

1. Skill name
2. Learning level: Beginner, Intermediate, or Advanced
3. Why the candidate should learn it
4. A practical next step or project to practice it

Return ONLY valid JSON in exactly this format:

{{
    "learning_pathway": [
        {{
            "skill": "",
            "level": "",
            "why": "",
            "next_step": ""
        }}
    ]
}}

Rules:
- Include every missing skill.
- Keep explanations concise and practical.
- The next step should be something the candidate can actually practice.
- Do not invent unrelated skills.
- Return ONLY JSON. No markdown or explanation.

Missing skills:
{missing_skills}
"""

    response = client.chat.completions.create(
        model="gemini-3.6-flash",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.choices[0].message.content

    try:
        result = result.strip()

        if result.startswith("```"):
            result = result.replace("```json", "").replace("```", "").strip()

        data = json.loads(result)

        pathway = data.get(
            "learning_pathway", []
        )

        return pathway

    except json.JSONDecodeError:
        return []