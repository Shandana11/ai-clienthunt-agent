import os
from crewai import Agent, Crew, LLM, Process, Task
from search_tool import FreeWebSearchTool

os.environ["LITELLM_RETRY"] = "True"

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

    # Back to your working model, but with a tiny max_tokens to prevent TPM limits
    llm = LLM(
        model="groq/openai/gpt-oss-20b",
        api_key=groq_api_key,
        temperature=0.1,
        max_tokens=200, 
    )

    search_tool = FreeWebSearchTool()

    client_hunt_agent = Agent(
        role="Researcher",
        goal="Find 2 remote jobs matching criteria.",
        backstory="Finds web opportunities quickly.",
        tools=[search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    # Ultra-short prompt to keep requested tokens very low (< 500 tokens)
    task_description = f"""
Find 2 remote gigs for:
- Skills: {skills}
- Type: {work_preference}
- Notes: {additional_requirements}

List: Title, Company, Link, Reason. Do not invent links.
"""

    research_task = Task(
        description=task_description,
        expected_output="A short list of 2 verified opportunities with links.",
        agent=client_hunt_agent,
    )

    crew = Crew(
        agents=[client_hunt_agent],
        tasks=[research_task],
        process=Process.sequential,
        verbose=False,
    )

    result = crew.kickoff()
    return str(result)
