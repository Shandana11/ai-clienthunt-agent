import streamlit as st
from clienthunt_agent import run_clienthunt

st.set_page_config(page_title="ClientHunt Agent", page_icon="🎯", layout="centered")

st.title("🎯 AI ClientHunt Agent")
st.write("Find freelance opportunities and generate tailored pitches automatically.")

# Automatically load Groq API Key from Streamlit Secrets
groq_api_key = None
try:
    if "GROQ_API_KEY" in st.secrets:
        groq_api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    pass

# Fallback to sidebar input only if secret is not set
if not groq_api_key:
    st.sidebar.header("Configuration")
    groq_api_key = st.sidebar.text_input("Groq API Key", type="password")

st.header("Search Parameters")
skills = st.text_input("Skills (e.g., Python, Streamlit, Graphic Design)")
experience = st.text_input("Experience Level")
work_preference = st.multiselect("Work Preference", ["Remote freelance projects", "Full-time", "Part-time"])
location_preference = st.text_input("Location Preference", value="Worldwide remote")
budget_preference = st.text_input("Budget Preference", value="Flexible")
additional_requirements = st.text_area("Additional Requirements")

if st.button("Find Opportunities"):
    if not groq_api_key:
        st.error("GROQ_API_KEY is missing. Add it in Streamlit Cloud Secrets.")
        st.stop()

    try:
        st.session_state.report = run_clienthunt(
            skills=skills,
            experience=experience,
            work_preference=", ".join(work_preference),
            location_preference=location_preference,
            budget_preference=budget_preference,
            additional_requirements=additional_requirements,
            groq_api_key=groq_api_key,
        )
        st.success("Search completed!")
    except Exception as error:
        st.error("Something went wrong while running the agent.")
        st.exception(error)

if "report" in st.session_state and st.session_state.report:
    st.subheader("ClientHunt Report")
    st.markdown(st.session_state.report)

    st.download_button(
        label="Download Report",
        data=st.session_state.report,
        file_name="clienthunt_report.txt",
        mime="text/plain",
    )
