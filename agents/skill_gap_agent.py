import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY")
)


def analyze_skill_gap(candidate_skills, target_career):

    prompt = f"""
You are a professional career skill gap analysis assistant.

Your task is to analyze a candidate's current skills against the skills
normally expected for their chosen target career.

IMPORTANT:
- The target career can be ANY legitimate career or profession.
- Do NOT assume the career is limited to technology or software.
- Careers may include software development, accounting, finance,
  marketing, sales, human resources, education, healthcare,
  design, business, management, engineering, law, operations,
  data analysis, etc.
- Determine the relevant skills specifically for the target career.
- Do not use a fixed predefined career list.

Candidate's current skills:
{candidate_skills}

Target career:
{target_career}

Identify the most important skills normally required for this career.

Return approximately 8-15 important skills.
Prioritize core and practically useful skills rather than listing
every possible skill.

Compare the required skills with the candidate's current skills.

A skill should be considered missing only when the candidate does not
already have that skill or a clearly equivalent skill.

Return ONLY valid JSON in exactly this format:

{{
    "required_skills": [],
    "missing_skills": []
}}

Rules:
- required_skills must contain 8-15 important skills for the target career.
- Skills must be relevant specifically to the target career.
- missing_skills must contain ONLY skills not already present in the candidate's skills.
- Do not include unrelated skills.
- Do not generate an unnecessarily large list.
- Keep skill names concise.
- Consider equivalent skill names where appropriate.
  Example: "Financial Analysis" and "Financial Analysis Skills"
  should be treated as the same skill.
- For non-technical careers, include domain-specific professional skills.
- For technical careers, include relevant technical and professional skills.
- Return ONLY JSON.
- No markdown.
- No explanation.

Candidate skills:
{candidate_skills}

Target career:
{target_career}
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
            result = (
                result
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        skills = json.loads(result)

        required_skills = skills.get("required_skills", [])
        missing_skills = skills.get("missing_skills", [])

        return required_skills, missing_skills

    except json.JSONDecodeError:
        return [], []