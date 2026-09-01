import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("GEMINI_API_KEY")
)


def discover_skills(resume_text):

    prompt = f"""
You are a professional resume skill extraction assistant.

Analyze the following resume and identify the candidate's skills.

Separate them into:

1. Technical skills
2. Transferable skills

Technical skills can include:
programming languages, frameworks, databases, tools,
cloud technologies, software, libraries, and technical concepts.

Transferable skills can include:
communication, teamwork, leadership, problem solving,
time management, adaptability, etc.

Return ONLY valid JSON in this exact format:

{{
    "technical_skills": [],
    "transferable_skills": []
}}

Resume:
{resume_text}
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
        skills = json.loads(result)

        technical_skills = skills.get(
            "technical_skills", []
        )

        transferable_skills = skills.get(
            "transferable_skills", []
        )

        return technical_skills, transferable_skills

    except json.JSONDecodeError:
        return [], []