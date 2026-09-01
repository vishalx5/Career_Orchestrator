import os
import json
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY")
)


def get_market_intelligence(target_career):

    prompt = f"""
You are a professional career market intelligence assistant.

Analyze the career:

{target_career}

Provide useful career-market information for this role.

Return ONLY valid JSON in exactly this format:

{{
    "demand": "",
    "top_skills": [],
    "growth": "",
    "opportunities": []
}}

Rules:
- demand should be one of: Low, Medium, High, or Very High.
- top_skills should contain important technical, non-technical, domain-specific, analytical, creative, or transferable skills relevant to this career.
- Skills must be appropriate for the specific career being analyzed.
- Do not assume the career is related to software development or technology.
- growth should briefly describe the general career growth outlook for this field.
- opportunities should contain relevant job titles or career opportunities related to this field.
- Keep the information concise and useful for a student or job seeker.
- Do not invent specific companies, salaries, statistics, or hiring information.
- Return ONLY JSON. No markdown or explanation.

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
            result = result.replace("```json", "").replace("```", "").strip()

        market_data = json.loads(result)

        demand = market_data.get("demand", "Medium")
        top_skills = market_data.get("top_skills", [])
        growth = market_data.get("growth", "")
        opportunities = market_data.get("opportunities", [])

        return {
            "demand": demand,
            "top_skills": top_skills,
            "growth": growth,
            "opportunities": opportunities
        }

    except json.JSONDecodeError:
        return {
            "demand": "Unknown",
            "top_skills": [],
            "growth": "Market information could not be generated.",
            "opportunities": []
        }