import os

import streamlit as st

from clienthunt_agent import run_clienthunt


st.set_page_config(
    page_title="AI ClientHunt Agent",
    page_icon="🔎",
    layout="wide",
)


def get_groq_api_key() -> str:
    """Read the Groq API key from Streamlit Secrets or environment variables."""
    try:
        secret_key = st.secrets.get("GROQ_API_KEY", "")
    except Exception:
        secret_key = ""

    return secret_key or os.getenv("GROQ_API_KEY", "")


st.title("🔎 AI ClientHunt Agent")

st.write(
    "Find relevant remote jobs and freelance opportunities "
    "using a single CrewAI agent."
)

st.info(
    "This app discovers public web results. "
    "Always verify the original listing before applying."
)

st.sidebar.header("Your Profile")

skills = st.sidebar.text_area(
    "Your skills",
    value=(
        "Generative AI, Agentic AI, Python, Streamlit, "
        "CrewAI, RAG, AI application development"
    ),
    height=120,
)

experience = st.sidebar.selectbox(
    "Experience level",
    [
        "Beginner",
        "Entry-level",
        "Intermediate",
        "Experienced",
    ],
)

work_preference = st.sidebar.multiselect(
    "Preferred work type",
    [
        "Remote freelance projects",
        "One-time projects",
        "Part-time remote work",
        "Full-time remote work",
        "Contract work",
    ],
    default=["Remote freelance projects", "One-time projects"],
)

location_preference = st.sidebar.selectbox(
    "Location preference",
    [
        "Worldwide remote",
        "Pakistan remote",
        "Remote - Asia",
        "Remote - Any location",
    ],
)

budget_preference = st.sidebar.text_input(
    "Income / project budget preference",
    placeholder="Example: $50-$500 per project",
)

additional_requirements = st.sidebar.text_area(
    "Additional requirements",
    placeholder=(
        "Example: Flexible hours, beginner-friendly, "
        "no paid connects, no daily office work"
    ),
    height=100,
)

st.subheader("Your Search Profile")

st.write("**Skills:**", skills)
st.write("**Experience:**", experience)
st.write("**Work preference:**", ", ".join(work_preference))
st.write("**Location:**", location_preference)

if st.button("🔍 Find Opportunities", type="primary"):
    if not skills.strip():
        st.error("Please enter at least one skill.")
        st.stop()

    groq_api_key = get_groq_api_key()

    if not groq_api_key:
        st.error(
            "GROQ_API_KEY is missing. Add it in Streamlit Cloud "
            "Settings → Secrets."
        )
        st.stop()

    with st.spinner(
        "The ClientHunt Agent is searching for opportunities..."
    ):
        try:
            report = run_clienthunt(
                skills=skills,
                experience=experience,
                work_preference=", ".join(work_preference),
                location_preference=location_preference,
                budget_preference=budget_preference,
                additional_requirements=additional_requirements,
                groq_api_key=groq_api_key,
            )

            st.success("Search completed!")

            st.subheader("📋 ClientHunt Report")
            st.markdown(report)

            st.download_button(
                label="📥 Download Report",
                data=report,
                file_name="clienthunt_report.md",
                mime="text/markdown",
            )

        except Exception as error:
            st.error("Something went wrong while running the agent.")
            st.exception(error)
