import os
from groq import Groq

def run_clienthunt(skills, experience, work_preference, location_preference, budget_preference, additional_requirements, groq_api_key):
    if not groq_api_key:
        return "Error: Groq API key is missing."

    client = Groq(api_key=groq_api_key)

    prompt = f"""
    You are an expert career and freelance strategist agent. Your task is to find matchable jobs, freelance projects, and work opportunities based on the user's specific profile and requirements.

    User Profile & Search Parameters:
    - Skills: {skills}
    - Experience Level: {experience}
    - Work Preference: {work_preference}
    - Location Preference: {location_preference}
    - Budget / Pay Preference: {budget_preference}
    - Additional Requirements: {additional_requirements}

    Please provide a comprehensive, structured report containing:
    1. **Top Matchable Platforms & Websites**: List specific platforms (e.g., Upwork, Contra, Remote.co, LinkedIn, etc.) where these exact skills and experience levels are in high demand.
    2. **Exact Workflows & Steps**: Provide a step-by-step workflow on how to target clients, optimize profiles, or apply on these platforms.
    3. **Tailored Pitch / Outreach Strategy**: Give a ready-to-use template or strategy for pitching clients.
    4. **Actionable Recommendations**: Clear, practical advice tailored to the user's experience level to land work quickly.

    Make the response professional, detailed, highly actionable, and easy to read using Markdown formatting.
    """

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a precise, highly skilled AI freelance and career matching assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2048,
        )
        
        report = response.choices[0].message.content
        return report

    except Exception as e:
        return f"An error occurred while generating the report via Groq: {str(e)}"
