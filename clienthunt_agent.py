import os
from groq import Groq

def run_clienthunt(
    skills,
    experience,
    work_preference,
    location_preference,
    budget_preference,
    additional_requirements,
    groq_api_key,
):
    if not groq_api_key:
        raise ValueError("Groq API key is missing.")

    # Initialize the official Groq client directly
    client = Groq(api_key=groq_api_key)

    prompt = f"""
You are an expert freelance career researcher. Find 2 active remote job or freelance opportunities matching these criteria:
- Skills: {skills}
- Experience: {experience}
- Work Type: {work_preference}
- Location: {location_preference}
- Budget/Rate: {budget_preference}
- Additional Notes: {additional_requirements}

Provide a clean, concise list including:
1. Job/Gig Title
2. Company or Platform
3. Direct Link (only verified, real links)
4. Brief Reason why it's a match
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {"role": "system", "content": "You are a helpful research assistant that provides accurate job leads with valid links."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.1,
        max_tokens=600,
    ]

    return response.choices[0].message.content
