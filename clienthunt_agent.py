import os

from crewai import Agent, Crew, LLM, Process, Task
from search_tool import FreeWebSearchTool


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

    os.environ["GROQ_API_KEY"] = groq_api_key

    llm = LLM(
        model="groq/openai/gpt-oss-20b",
        api_key=groq_api_key,
        temperature=0.1,
        max_tokens=500,
    )

    search_tool = FreeWebSearchTool()

    client_hunt_agent = Agent(
        role="AI ClientHunt Research Specialist",
        goal=(
            "Find relevant remote jobs, freelance projects, "
            "and potential clients based on the user's requirements."
        ),
        backstory=(
            "You are an opportunity research specialist. "
            "You search the public web and do not invent information."
        ),
        tools=[search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    task_description = f"""
Find relevant online work opportunities based on these details:

Skills: {skills}
Experience: {experience}
Work preference: {work_preference}
Location: {location_preference}
Budget: {budget_preference}
Additional requirements: {additional_requirements}

Search for realistic remote jobs, freelance projects,
internships, and potential clients matching the user's skills.

For each opportunity, provide:
1. Title
2. Company or client
3. Source website and application link, if available
4. Brief matching reason
5. Application advice

Return a concise report with up to 5 opportunities.
Do not invent jobs, companies, links, salaries, or deadlines.
"""

    research_task = Task(
        description=task_description,
        expected_output=(
            "A concise report with up to 5 relevant opportunities. "
            "Include the title, company, source link, matching reason, "
            "and application advice. Do not invent information."
        ),
        agent=client_hunt_agent,
    )

    crew = Crew(
        agents=[client_hunt_agent],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    return str(result)
