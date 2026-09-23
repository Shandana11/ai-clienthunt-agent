import os
from crewai import Agent, Crew, LLM, Process, Task
from search_tool import FreeWebSearchTool

# 1. Force LiteLLM to auto-wait and retry if a rate limit happens
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

    # 2. Switched to Llama 3.1 8B which has a much higher free token limit (500K TPD) 
    # and lower overhead than the 20B reasoning model.
    llm = LLM(
        model="groq/meta-llama/llama-3.1-8b-instant",
        api_key=groq_api_key,
        temperature=0.1,
        max_tokens=400,
    )

    search_tool = FreeWebSearchTool()

    # 3. Minimized system prompt instructions to save tokens per request
    client_hunt_agent = Agent(
        role="Opportunity Researcher",
        goal="Find relevant remote jobs and freelance projects matching user criteria.",
        backstory="You search the web accurately and provide concise opportunity reports.",
        tools=[search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    task_description = f"""
Find up to 3 remote jobs or freelance projects:
- Skills: {skills}
- Experience: {experience}
- Type: {work_preference}
- Location: {location_preference}
- Budget: {budget_preference}
- Notes: {additional_requirements}

For each opportunity list: Title, Company/Client, Link, Reason, and Advice. Do not invent links.
"""

    research_task = Task(
        description=task_description,
        expected_output="A concise list of up to 3 web-verified opportunities with titles, links, and details.",
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
