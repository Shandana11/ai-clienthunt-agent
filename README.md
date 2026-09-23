# 🔎 AI ClientHunt Agent

A beginner-friendly AI-powered job discovery assistant built with
CrewAI, Groq, Streamlit, and free public web search.

## Features

- Single CrewAI agent
- Groq LLM integration
- Groq model: `openai/gpt-oss-120b`
- Free public web search
- Skill and experience matching
- Remote and freelance opportunity research
- Markdown report generation
- Streamlit user interface
- Downloadable report

## Project Structure

```text
ai-clienthunt-agent/
├── app.py
├── clienthunt_agent.py
├── search_tool.py
├── requirements.txt
├── .gitignore
├── README.md
└── .streamlit/
    └── secrets.toml.example
```

## Deployment

This project is designed for Streamlit Community Cloud.

1. Upload the project files to GitHub.
2. Open Streamlit Community Cloud.
3. Create a new app from the GitHub repository.
4. Select `app.py` as the main file.
5. Open the app settings.
6. Add this secret:

```toml
GROQ_API_KEY = "your_actual_groq_api_key"
```

Do not upload your real API key to GitHub.

## Important Limitations

- The app searches publicly available web results.
- Some websites may block automated searches.
- Search results may be outdated or incomplete.
- A search result does not guarantee that a job is still active.
- The app does not automatically apply for jobs.
- Always verify the original listing before applying.

## Technologies

- Python
- CrewAI
- Groq
- Streamlit
- DDGS web search
- Pydantic
