import os
import json
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY")
)


def match_jobs(candidate_skills, target_career):

    prompt = f"""
You are a professional AI job matching assistant.

The candidate has these skills:

{candidate_skills}

The candidate wants to pursue this career:

{target_career}

Generate a list of realistic job opportunities that match the candidate's
skills and target career.

Return ONLY valid JSON in exactly this format:

{{
    "jobs": [
        {{
            "title": "",
            "company": "",
            "location": "",
            "skills": [],
            "type": "",
            "matching_skills": [],
            "match_percentage": 0
        }}
    ]
}}

Rules:
- Generate 4 to 6 relevant job opportunities.
- Jobs must be relevant to the target career.
- Jobs can belong to ANY professional field, including technology,
  business, finance, accounting, marketing, sales, HR, education,
  healthcare, design, engineering, and other fields.
- Use realistic but clearly fictional company names.
- Do not claim that the companies or jobs are real.
- Location can be Remote, Hybrid, or a city.
- Type can be Full-time, Part-time, Internship, or Contract.
- Skills should contain the important skills normally required for that job.
- Skills can be technical, non-technical, domain-specific, analytical,
  creative, communication-based, or transferable.
- matching_skills should contain ONLY skills that the candidate already has.
- Do not include skills in matching_skills that are not present in the
  candidate's skills.
- Match skill names case-insensitively when comparing skills.
- match_percentage should be between 0 and 100.
- Calculate match_percentage based on how many required job skills
  match the candidate's existing skills.
- Do not invent real company hiring information.
- Do not provide URLs.
- Return ONLY JSON. No markdown or explanation.

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
            result = result.replace("```json", "").replace("```", "").strip()

        data = json.loads(result)

        jobs = data.get("jobs", [])

        # Make sure match percentages are valid
        for job in jobs:
            percentage = job.get("match_percentage", 0)

            try:
                percentage = float(percentage)
            except (ValueError, TypeError):
                percentage = 0

            percentage = max(0, min(100, percentage))
            job["match_percentage"] = round(percentage)

        # Sort highest match first
        jobs.sort(
            key=lambda job: job.get("match_percentage", 0),
            reverse=True
        )

        return jobs

    except json.JSONDecodeError:
        return []