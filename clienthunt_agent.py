
import os

import crewai.llms.cache as _crewai_cache

# Workaround for CrewAI cache_breakpoint error with Groq
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

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

    # Set the Groq API key
    os.environ["GROQ_API_KEY"] = groq_api_key

    # Initialize the Groq LLM
    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=groq_api_key,
        temperature=0.2,
    )

    # Initialize the web search tool
    search_tool = FreeWebSearchTool()

    # Create the ClientHunt AI agent
    client_hunt_agent = Agent(
        role="AI ClientHunt Research Specialist",
        goal=(
            "Find relevant remote job opportunities, freelance projects, "
            "and potential clients based on the user's skills, experience, "
            "preferences, and requirements."
        ),
        backstory=(
            "You are an expert opportunity researcher who searches the "
            "public web for relevant and realistic opportunities. You "
            "carefully analyze job listings and provide useful details "
            "without inventing information."
        ),
        tools=[search_tool],
        llm=llm,
        verbose=True,
        allow_delegation=False,
    )

    # Prepare the research task
    task_description = f"""
    Find relevant online work opportunities based on the following user
    information:

    Skills:
    {skills}

    Experience:
    {experience}

    Work preference:
    {work_preference}

    Location preference:
    {location_preference}

    Budget or expected payment:
    {budget_preference}

    Additional requirements:
    {additional_requirements}

    Your responsibilities:

    1. Search the public web for relevant remote jobs, freelance projects,
       internships, and potential clients.

    2. Focus on opportunities that match the user's skills and experience.

    3. Prioritize realistic opportunities for the user's experience level.

    4. Provide the opportunity title and company or client name when available.

    5. Include the source website and direct application link when available.

    6. Explain why each opportunity may be relevant.

    7. Do not invent job listings, companies, links, salaries, or deadlines.

    8. Clearly mention when information cannot be verified.

    9. Present the results in a clear and organized format.

    10. Provide practical suggestions for applying or contacting the client.

    Return a useful opportunity research report for the user.
    """

    research_task = Task(
        description=task_description,
        expected_output=(
            "A clear and organized report containing relevant opportunities, "
            "source links, matching reasons, and practical application advice."
        ),
        agent=client_hunt_agent,
    )

    # Create and run the CrewAI crew
    crew = Crew(
        agents=[client_hunt_agent],
        tasks=[research_task],
        process=Process.sequential,
        verbose=True,
    )

    result = crew.kickoff()

    return str(result)
