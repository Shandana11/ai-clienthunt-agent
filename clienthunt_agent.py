from crewai import Agent, Crew, LLM, Process, Task

from search_tool import FreeWebSearchTool


def run_clienthunt(
    skills: str,
    experience: str,
    work_preference: str,
    location_preference: str,
    budget_preference: str,
    additional_requirements: str,
    groq_api_key: str,
) -> str:
    """Run one CrewAI agent to discover and analyze opportunities."""

    if not groq_api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Configure it in Streamlit Secrets."
        )

    llm = LLM(
        model="groq/openai/gpt-oss-120b",
        api_key=groq_api_key,
        temperature=0.2,
    )

    search_tool = FreeWebSearchTool()

    client_hunt_agent = Agent(
        role="AI Client Hunting Specialist",
        goal=(
            "Find relevant and publicly discoverable job opportunities "
            "for the user's skills and preferences."
        ),
        backstory=(
            "You are a careful job research assistant specializing in "
            "remote work, freelance projects, AI development, automation, "
            "and beginner-friendly client leads. You evaluate search "
            "results based on the user's actual skills and experience. "
            "You never invent job listings or claim that a listing is "
            "still open without evidence."
        ),
        llm=llm,
        tools=[search_tool],
        verbose=True,
        allow_delegation=False,
    )

    task_description = f"""
Find relevant job and freelance opportunities based on this profile.

USER SKILLS:
{skills}

EXPERIENCE:
{experience}

WORK PREFERENCE:
{work_preference}

LOCATION PREFERENCE:
{location_preference}

BUDGET / INCOME PREFERENCE:
{budget_preference}

ADDITIONAL REQUIREMENTS:
{additional_requirements}

INSTRUCTIONS:
1. Search the public web using the available search tool.
2. Search across different websites and platforms.
3. Include job boards, company career pages, and freelance opportunities.
4. Focus on the user's actual skills and experience.
5. Prefer opportunities matching the user's work preferences.
6. Never invent job titles, companies, URLs, salaries, or requirements.
7. Avoid duplicate results.
8. Explain why each opportunity may match the profile.
9. Identify missing information and possible risks.
10. Include the original source URL for every opportunity.

Return a clear markdown report with:
- Opportunity title
- Company or platform
- Source URL
- Work type
- Required skills
- Experience requirements
- Match explanation
- Important limitations or risks
- Suggested next action

IMPORTANT:
A search result is not proof that a job is currently active.
Clearly distinguish discovered listings from verified active opportunities.
Do not apply to jobs or contact clients automatically.
"""

    research_task = Task(
        description=task_description,
        expected_output=(
            "A structured markdown report of relevant job opportunities "
            "with source URLs, matching explanations, and limitations."
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
